#!/usr/bin/env python3
"""
Cloudflare Rules Deployer
Deploys WAF and Cache rules to Cloudflare zones via API based on profile definitions and sites.json inventory.

Usage:
  python3 deploy.py --site afarma.it
  python3 deploy.py --site afarma.it --tier attack
  python3 deploy.py --zone elidelagenzia.com --profile wordpress
  python3 deploy.py --list-sites
  python3 deploy.py --all [--waf-only] [--tier standard|attack]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
RULES_DIR = os.path.join(SRC_DIR, "rules")
PROFILES_DIR = os.path.join(SRC_DIR, "profiles")
SITES_FILE = os.path.join(BASE_DIR, "sites.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_sites_inventory():
    if os.path.exists(SITES_FILE):
        return load_json(SITES_FILE)
    return {}


def cf_api_request(endpoint, token, method="GET", data=None):
    url = f"https://api.cloudflare.com/client/v4/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            return json.loads(error_body)
        except Exception:
            return {"success": False, "errors": [{"message": f"HTTP {e.code}: {error_body}"}]}
    except Exception as e:
        return {"success": False, "errors": [{"message": str(e)}]}


def resolve_zone_id(zone_input, token):
    # Check if already a 32-char hex ID
    if len(zone_input) == 32 and all(c in "0123456789abcdefABCDEF" for c in zone_input):
        return zone_input, zone_input

    # Query Cloudflare API by zone name
    res = cf_api_request(f"zones?name={zone_input.strip()}", token)
    if not res.get("success") or not res.get("result"):
        print(f"Error: Could not resolve zone '{zone_input}': {res.get('errors')}", file=sys.stderr)
        sys.exit(1)

    zone_info = res["result"][0]
    return zone_info["id"], zone_info["name"]


def build_waf_payload(profile, zone_name="", tier="standard"):
    title = profile["title"].upper()
    rule_ids = profile["waf"]["whitelist"]
    rules = []
    for r_id in rule_ids:
        r_path = os.path.join(RULES_DIR, "waf", f"{r_id}.json")
        rules.append(load_json(r_path))

    whitelist_expr = " or ".join([f"({r['expression']})" for r in rules])

    waf_rules = [
        {
            "action": "skip",
            "action_parameters": {
                "phases": [
                    "http_ratelimit",
                    "http_request_firewall_managed",
                    "http_request_sbfm"
                ],
                "products": [
                    "bic",
                    "zoneLockdown",
                    "rateLimit",
                    "waf",
                    "securityLevel",
                    "hot",
                    "uaBlock"
                ],
                "ruleset": "current"
            },
            "description": f"WHITELIST - {title}",
            "enabled": True,
            "expression": whitelist_expr,
            "logging": {
                "enabled": True
            }
        }
    ]

    # 2. VERIFYLIST (Countries challenge)
    if "verifylist" in profile["waf"]:
        vl_id = profile["waf"]["verifylist"]
        vl_path = os.path.join(RULES_DIR, "waf", f"{vl_id}.json")
        vl_rule = load_json(vl_path)
        waf_rules.append({
            "action": vl_rule.get("action", "managed_challenge"),
            "description": f"VERIFYLIST - {title}",
            "enabled": True,
            "expression": vl_rule["expression"]
        })

    # 3. BLACKLIST (Referer & Search block 403)
    # Tier 'standard': rule is created but disabled (enabled: False) to prevent false positives.
    # Tier 'attack': rule is active (enabled: True) to mitigate intense L7/scraping flood.
    if "blacklist" in profile["waf"]:
        bl_id = profile["waf"]["blacklist"]
        bl_path = os.path.join(RULES_DIR, "waf", f"{bl_id}.json")
        bl_rule = load_json(bl_path)
        bl_expr = bl_rule["expression"]
        if zone_name:
            bl_expr = bl_expr.replace("{DOMAIN}", zone_name)

        is_attack_tier = (tier == "attack")
        waf_rules.append({
            "action": bl_rule.get("action", "block"),
            "description": f"BLACKLIST - {title}",
            "enabled": is_attack_tier,
            "expression": bl_expr
        })

    return {"rules": waf_rules}


def build_cache_payload(profile):
    title = profile["title"].upper()
    fpc_id = profile["cache"]["fpc"]
    fpc_data = load_json(os.path.join(RULES_DIR, "cache", f"{fpc_id}.json"))

    bypass_id = profile["cache"]["bypass"]
    bypass_data = load_json(os.path.join(RULES_DIR, "cache", f"{bypass_id}.json"))

    bypass_expr = " or ".join([f"({item['expr']})" for item in bypass_data["items"]])

    # Notice: In Cloudflare Cache Rules, latter rules override earlier rules.
    # Rule 1: FPC (Cache Everything for GET/HEAD)
    # Rule 2: Bypass (CMS exceptions, positioned second for override)
    return {
        "rules": [
            {
                "action": fpc_data["action"],
                "action_parameters": fpc_data["action_parameters"],
                "description": f"FULL PAGE CACHE (FPC) - {title}",
                "enabled": True,
                "expression": fpc_data["expression"]
            },
            {
                "action": bypass_data["action"],
                "action_parameters": bypass_data["action_parameters"],
                "description": f"CACHE WHITELIST (BYPASS) - {title}",
                "enabled": True,
                "expression": bypass_expr
            }
        ]
    }


def deploy_single_zone(zone_input, profile_name, tier, token, waf_only=False, cache_only=False, dry_run=False):
    profile_path = os.path.join(PROFILES_DIR, f"{profile_name}.json")
    if not os.path.exists(profile_path):
        print(f"Error: Profile '{profile_name}' not found in {PROFILES_DIR}", file=sys.stderr)
        return False

    profile = load_json(profile_path)
    deploy_waf = not cache_only
    deploy_cache = not waf_only

    zone_id = None
    zone_name = zone_input
    if not dry_run:
        print(f"\nResolving zone '{zone_input}'...")
        zone_id, zone_name = resolve_zone_id(zone_input, token)
        print(f"Target Zone: {zone_name} (ID: {zone_id})")

    print(f"Profile: {profile['title']} ({profile_name}) | Security Tier: {tier.upper()}")
    if tier == "standard":
        print("  -> BLACKLIST rule state: INACTIVE (enabled: false) - Standby mode")
    else:
        print("  -> BLACKLIST rule state: ACTIVE (enabled: true) - Under Attack protection")

    # 1. WAF Deployment
    if deploy_waf:
        print("\n--- [WAF RULES] ---")
        waf_payload = build_waf_payload(profile, zone_name, tier=tier)
        if dry_run:
            print("[DRY-RUN] WAF Payload:")
            print(json.dumps(waf_payload, indent=2))
        else:
            print("Deploying WAF ruleset (phase: http_request_firewall_custom)...")
            res = cf_api_request(
                f"zones/{zone_id}/rulesets/phases/http_request_firewall_custom/entrypoint",
                token,
                method="PUT",
                data=waf_payload
            )
            if res.get("success"):
                rules_count = len(res['result']['rules'])
                print(f"  SUCCESS! WAF rules updated (Ruleset ID: {res['result']['id']}, Rules: {rules_count})")
            else:
                print(f"  FAILED to update WAF rules: {res.get('errors')}", file=sys.stderr)
                return False

    # 2. Cache Deployment
    if deploy_cache:
        print("\n--- [CACHE RULES] ---")
        cache_payload = build_cache_payload(profile)
        if dry_run:
            print("[DRY-RUN] Cache Payload:")
            print(json.dumps(cache_payload, indent=2))
        else:
            print("Deploying Cache ruleset (phase: http_request_cache_settings)...")
            res = cf_api_request(
                f"zones/{zone_id}/rulesets/phases/http_request_cache_settings/entrypoint",
                token,
                method="PUT",
                data=cache_payload
            )
            if res.get("success"):
                rules_count = len(res['result']['rules'])
                print(f"  SUCCESS! Cache rules updated (Ruleset ID: {res['result']['id']}, Rules: {rules_count})")
            else:
                print(f"  FAILED to update Cache rules: {res.get('errors')}", file=sys.stderr)
                return False

    print(f"Deployment to '{zone_name}' completed successfully!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Deploy Cloudflare rules from profile and sites.json inventory")
    parser.add_argument("--site", help="Site domain from sites.json (e.g. afarma.it)")
    parser.add_argument("--zone", help="Zone name (e.g. example.com) or 32-char Zone ID")
    parser.add_argument("--profile", help="Profile name (e.g. wordpress, woocommerce, magento1, magento2, prestashop)")
    parser.add_argument("--tier", choices=["standard", "attack"], help="Security tier: standard (BLACKLIST disabled) or attack (BLACKLIST active 403)")
    parser.add_argument("--token", default=None, help="Cloudflare API Token (defaults to $CF_API_TOKEN)")
    parser.add_argument("--waf-only", action="store_true", help="Deploy only WAF rules")
    parser.add_argument("--cache-only", action="store_true", help="Deploy only Cache rules")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without deploying to Cloudflare")
    parser.add_argument("--list-sites", action="store_true", help="List all sites configured in sites.json")
    parser.add_argument("--all", action="store_true", help="Deploy to all sites configured in sites.json")

    args = parser.parse_args()
    sites = load_sites_inventory()

    if args.list_sites:
        print("\n=== SITES INVENTORY (sites.json) ===")
        print(f"{'Domain':<30} {'Profile':<15} {'Tier':<10} {'Description'}")
        print("-" * 75)
        for domain, info in sorted(sites.items()):
            print(f"{domain:<30} {info.get('profile', ''):<15} {info.get('tier', 'standard'):<10} {info.get('description', '')}")
        print("-" * 75)
        print(f"Total sites: {len(sites)}\n")
        return

    token = args.token or os.environ.get("CF_API_TOKEN")
    if not token and not args.dry_run:
        print("Error: Cloudflare API token not provided. Set $CF_API_TOKEN or use --token.", file=sys.stderr)
        sys.exit(1)

    # Batch deployment to all sites in sites.json
    if args.all:
        if not sites:
            print("Error: No sites found in sites.json", file=sys.stderr)
            sys.exit(1)
        print(f"\nStarting batch deployment for {len(sites)} site(s)...")
        success_count = 0
        for domain, info in sites.items():
            profile_name = info.get("profile")
            tier = args.tier or info.get("tier", "standard")
            ok = deploy_single_zone(domain, profile_name, tier, token, args.waf_only, args.cache_only, args.dry_run)
            if ok:
                success_count += 1
        print(f"\nBatch deployment completed: {success_count}/{len(sites)} sites successful.")
        return

    # Single site resolution
    target_site = args.site or args.zone
    if not target_site:
        print("Error: Specify --site <domain>, --zone <domain>, --all, or --list-sites.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    site_info = sites.get(target_site, {})
    profile_name = args.profile or site_info.get("profile")
    if not profile_name:
        print(f"Error: Profile not specified and '{target_site}' not found in sites.json. Use --profile.", file=sys.stderr)
        sys.exit(1)

    tier = args.tier or site_info.get("tier", "standard")

    deploy_single_zone(target_site, profile_name, tier, token, args.waf_only, args.cache_only, args.dry_run)


if __name__ == "__main__":
    main()
