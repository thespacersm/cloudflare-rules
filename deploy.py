#!/usr/bin/env python3
"""
Cloudflare Rules Deployer
Deploys WAF and Cache rules to Cloudflare zones via API based on profile definitions.

Usage:
  python3 deploy.py --zone elidelagenzia.com --profile wordpress
  python3 deploy.py --zone <domain_or_id> --profile <profile> [--waf-only] [--cache-only] [--dry-run]
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


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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


def build_waf_payload(profile):
    title = profile["title"].upper()
    rule_ids = profile["waf"]["whitelist"]
    rules = []
    for r_id in rule_ids:
        r_path = os.path.join(RULES_DIR, "waf", f"{r_id}.json")
        rules.append(load_json(r_path))

    whitelist_expr = " or ".join([f"({r['expression']})" for r in rules])

    cb_id = profile["waf"].get("country_block", "country-block")
    cb_path = os.path.join(RULES_DIR, "waf", f"{cb_id}.json")
    cb_rule = load_json(cb_path)

    return {
        "rules": [
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
            },
            {
                "action": "managed_challenge",
                "description": cb_rule["name"],
                "enabled": True,
                "expression": cb_rule["expression"]
            }
        ]
    }


def build_cache_payload(profile):
    title = profile["title"].upper()
    fpc_id = profile["cache"]["fpc"]
    fpc_data = load_json(os.path.join(RULES_DIR, "cache", f"{fpc_id}.json"))

    bypass_id = profile["cache"]["bypass"]
    bypass_data = load_json(os.path.join(RULES_DIR, "cache", f"{bypass_id}.json"))

    bypass_expr = " or ".join([f"({item['expr']})" for item in bypass_data["items"]])

    # Notice: In Cloudflare Cache Rules, latter rules override earlier rules.
    # Rule 1: FPC (Cache Everything for GET/HEAD)
    # Rule 2: Bypass (WordPress/WooCommerce exceptions, positioned second for override)
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


def main():
    parser = argparse.ArgumentParser(description="Deploy Cloudflare rules from profile")
    parser.add_argument("--zone", required=True, help="Zone name (e.g. example.com) or 32-char Zone ID")
    parser.add_argument("--profile", required=True, help="Profile name (e.g. wordpress, woocommerce, magento1, magento2, prestashop)")
    parser.add_argument("--token", default=None, help="Cloudflare API Token (defaults to $CF_API_TOKEN)")
    parser.add_argument("--waf-only", action="store_true", help="Deploy only WAF rules")
    parser.add_argument("--cache-only", action="store_true", help="Deploy only Cache rules")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without deploying to Cloudflare")

    args = parser.parse_args()

    token = args.token or os.environ.get("CF_API_TOKEN")
    if not token and not args.dry_run:
        print("Error: Cloudflare API token not provided. Set $CF_API_TOKEN or use --token.", file=sys.stderr)
        sys.exit(1)

    profile_path = os.path.join(PROFILES_DIR, f"{args.profile}.json")
    if not os.path.exists(profile_path):
        print(f"Error: Profile '{args.profile}' not found in {PROFILES_DIR}", file=sys.stderr)
        sys.exit(1)

    profile = load_json(profile_path)
    deploy_waf = not args.cache_only
    deploy_cache = not args.waf_only

    zone_id = None
    zone_name = args.zone
    if not args.dry_run:
        print(f"Resolving zone '{args.zone}'...")
        zone_id, zone_name = resolve_zone_id(args.zone, token)
        print(f"Target Zone: {zone_name} (ID: {zone_id})")

    print(f"Selected Profile: {profile['title']} ({args.profile})")

    # 1. WAF Deployment
    if deploy_waf:
        print("\n--- [WAF RULES] ---")
        waf_payload = build_waf_payload(profile)
        if args.dry_run:
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
                print(f"  SUCCESS! WAF rules updated (Ruleset ID: {res['result']['id']}, Rules: {len(res['result']['rules'])})")
            else:
                print(f"  FAILED to update WAF rules: {res.get('errors')}", file=sys.stderr)
                sys.exit(1)

    # 2. Cache Deployment
    if deploy_cache:
        print("\n--- [CACHE RULES] ---")
        cache_payload = build_cache_payload(profile)
        if args.dry_run:
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
                print(f"  SUCCESS! Cache rules updated (Ruleset ID: {res['result']['id']}, Rules: {len(res['result']['rules'])})")
            else:
                print(f"  FAILED to update Cache rules: {res.get('errors')}", file=sys.stderr)
                sys.exit(1)

    print(f"\nAll requested rules successfully deployed to '{zone_name}'!")


if __name__ == "__main__":
    main()
