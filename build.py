#!/usr/bin/env python3
"""
Cloudflare Rules Builder
Generates Markdown rulebooks for CMS platforms from reusable JSON components.
Usage: python3 build.py
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
RULES_DIR = os.path.join(SRC_DIR, "rules")
PROFILES_DIR = os.path.join(SRC_DIR, "profiles")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_waf_whitelist(profile):
    title = profile["title"].upper()
    rule_ids = profile["waf"]["whitelist"]
    rules = []
    for r_id in rule_ids:
        r_path = os.path.join(RULES_DIR, "waf", f"{r_id}.json")
        if not os.path.exists(r_path):
            print(f"Error: Rule not found: {r_path}", file=sys.stderr)
            sys.exit(1)
        rules.append(load_json(r_path))

    md = f"# WAF WHITELIST - {title}\n\n"
    md += "### Azione\n"
    md += "`Skip`\n"
    md += "- Skip all remaining rules in current ruleset\n"
    md += "- Phase: `http_ratelimit`, `http_request_firewall_managed`, `http_request_sbfm`\n"
    md += "- Products: `WAF`, `Rate Limiting`, `Security Level`, `Zone Lockdown`, `User Agent Blocking`, `Browser Integrity Check`\n\n"
    md += "---\n\n"
    md += "### Regole e Condizioni con Commenti\n\n"

    for r in rules:
        md += f"#### {r['name']}\n"
        md += f"{r['description']}\n"
        md += "```text\n"
        md += f"{r['expression']}\n"
        md += "```\n\n"

    md += "---\n\n"
    md += "### Tabella di Riepilogo\n\n"
    md += "| Categoria | Condizione | Dettaglio / Note |\n"
    md += "| :--- | :--- | :--- |\n"
    for r in rules:
        md += f"| **{r['category']}** | `{r['expression']}` | {r['note']} |\n"

    md += "\n---\n\n"
    md += "### Espressione Completa (Cloudflare Expression Builder)\n\n"
    md += "```text\n"
    exprs = [f"({r['expression']})" for r in rules]
    md += " or ".join(exprs) + "\n"
    md += "```\n"

    return md


def build_waf_blacklist(profile):
    bl_id = profile["waf"].get("blacklist", f"blacklist-{profile['platform']}")
    bl_path = os.path.join(RULES_DIR, "waf", f"{bl_id}.json")
    rule = load_json(bl_path)
    title = profile["title"].upper()

    md = f"# BLACKLIST - {title}\n\n"
    md += "### Azione Cloudflare (WAF Custom Rule)\n"
    md += f"* **Azione**: `{rule.get('action_label', 'Verifica interattiva (Interactive Challenge)')}` (`action: {rule.get('action', 'interactive_challenge')}`)\n\n"
    md += f"### Descrizione\n{rule['description']}\n\n"
    md += "---\n\n"
    md += "### Condizioni Dettagliate con Commenti\n\n"

    for c in rule.get("conditions", []):
        md += f"#### {c['title']}\n"
        md += f"{c['desc']}\n"
        md += "```text\n"
        md += f"{c['expr']}\n"
        md += "```\n\n"

    md += "---\n\n"
    md += "### Espressione Completa (Cloudflare Expression Builder)\n\n"
    if "{DOMAIN}" in rule["expression"]:
        md += "> [!NOTE]\n"
        md += "> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).\n\n"
    md += "```text\n"
    md += f"{rule['expression']}\n"
    md += "```\n"

    return md


def build_cache_whitelist(profile):
    bypass_id = profile["cache"]["bypass"]
    b_path = os.path.join(RULES_DIR, "cache", f"{bypass_id}.json")
    bypass_data = load_json(b_path)
    title = profile["title"].upper()

    md = f"# CACHE WHITELIST (BYPASS CACHE) - {title}\n\n"
    md += f"{bypass_data['description']}\n\n"
    md += "### Posizione nella Ruleset\n"
    md += "Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.\n"
    md += "Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.\n\n"
    md += "### Azione Cloudflare (Cache Rule)\n"
    md += "* **Eligible for cache**: `Bypass cache` (`cache: false`)\n\n"
    md += "---\n\n"
    md += "### Condizioni Dettagliate con Commenti\n\n"

    for i, item in enumerate(bypass_data["items"], 1):
        md += f"#### {i}. {item['title']}\n"
        md += f"{item['desc']}\n"
        md += "```text\n"
        md += f"{item['expr']}\n"
        md += "```\n\n"

    md += "---\n\n"
    md += "### Tabella di Riepilogo\n\n"
    md += "| Ambito | Condizione | Motivazione |\n"
    md += "| :--- | :--- | :--- |\n"
    for item in bypass_data["items"]:
        md += f"| **{item['title']}** | `{item['expr']}` | {item['desc']} |\n"

    md += "\n---\n\n"
    md += "### Espressione Completa (Bypass Cache)\n\n"
    md += "```text\n"
    exprs = [f"({item['expr']})" for item in bypass_data["items"]]
    md += " or ".join(exprs) + "\n"
    md += "```\n"

    return md


def build_cache_fpc(profile):
    fpc_id = profile["cache"]["fpc"]
    fpc_path = os.path.join(RULES_DIR, "cache", f"{fpc_id}.json")
    fpc_data = load_json(fpc_path)

    bypass_id = profile["cache"]["bypass"]
    b_path = os.path.join(RULES_DIR, "cache", f"{bypass_id}.json")
    bypass_data = load_json(b_path)

    title = profile["title"].upper()

    standalone_exclusions = " or ".join([item["expr"] for item in bypass_data["items"]])

    md = f"# FULL PAGE CACHE (FPC) - {title}\n\n"
    md += f"Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare. Nella logica a due regole, questa regola memorizza in cache **tutto il traffico pubblico**, poiché tutte le pagine dinamiche, carrelli e sessioni sono già state intercettate e skippate dalla regola **Cache Whitelist (Bypass)**.\n\n"
    md += "### Ordine di Esecuzione delle Regole (Cloudflare Cache Rules)\n"
    md += "Nel Ruleset Engine di Cloudflare per le Cache Rules, **l'ultima regola che matcha ha la precedenza** (sovrascrive le impostazioni delle precedenti).\n\n"
    md += "Pertanto, l'ordine di inserimento è:\n"
    md += "1. **Regola 1 (FPC - Cache Everything)**: abilita la cache su tutte le richieste pubbliche `http.request.method in {\"GET\" \"HEAD\"}`.\n"
    md += "2. **Regola 2 (Whitelist - Bypass Cache)**: posizionata **sotto/dopo** l'FPC, intercetta le eccezioni del CMS (carrello, admin, login, cookie) e imposta `Bypass cache` (`cache: false`), sovrascrivendo l'FPC.\n\n"
    md += "---\n\n"
    md += "### Azione Cloudflare (Cache Rule)\n"
    md += "* **Eligible for cache**: `Cache everything` (`cache: true`)\n"
    md += "* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno) o personalizzato\n"
    md += "* **Browser TTL**: `Respect origin`\n"
    md += "* **Cache Key**:\n"
    md += "  * Query String: `Ignore query string` (oppure personalizzata escludendo parametri di tracking come `fbclid`, `gclid`, `utm_*`)\n\n"
    md += "---\n\n"
    md += "### Espressione Principale (Modello a 2 Regole)\n\n"
    md += "Poiché le eccezioni dinamiche sono gestite a monte da `WHITELIST.md`, l'espressione per cachare tutto il traffico pubblico è semplicemente:\n\n"
    md += "#### 1. Metodi HTTP Idonei alla Cache\n"
    md += f"{fpc_data['description']}\n"
    md += "```text\n"
    md += f"{fpc_data['expression']}\n"
    md += "```\n\n"
    md += "---\n\n"
    md += "### Variante Standalone (Regola Singola con Esclusioni Integrate)\n\n"
    md += "Se preferisci creare una sola regola anziché due separate, puoi inserire le esclusioni direttamente nell'FPC:\n\n"
    md += "```text\n"
    md += f"({fpc_data['expression']} and not ({standalone_exclusions}))\n"
    md += "```\n"

    return md


def main():
    profile_files = sorted([f for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])
    if not profile_files:
        print("No profiles found in src/profiles/")
        return

    print(f"Found {len(profile_files)} profile(s) to compile: {', '.join(profile_files)}")

    for p_file in profile_files:
        profile_path = os.path.join(PROFILES_DIR, p_file)
        profile = load_json(profile_path)
        platform = profile["platform"]
        print(f"\nBuilding [{platform}]...")

        dest_waf = os.path.join(BASE_DIR, "build", platform, "waf")
        dest_cache = os.path.join(BASE_DIR, "build", platform, "cache")
        os.makedirs(dest_waf, exist_ok=True)
        os.makedirs(dest_cache, exist_ok=True)

        # 1. WAF Whitelist
        waf_whitelist_md = build_waf_whitelist(profile)
        with open(os.path.join(dest_waf, "WHITELIST.md"), "w", encoding="utf-8") as f:
            f.write(waf_whitelist_md)
        print(f"  -> build/{platform}/waf/WHITELIST.md")

        # 2. WAF Blacklist
        waf_blacklist_md = build_waf_blacklist(profile)
        with open(os.path.join(dest_waf, "BLACKLIST.md"), "w", encoding="utf-8") as f:
            f.write(waf_blacklist_md)
        print(f"  -> build/{platform}/waf/BLACKLIST.md")

        # 3. Cache Whitelist (Bypass)
        cache_whitelist_md = build_cache_whitelist(profile)
        with open(os.path.join(dest_cache, "WHITELIST.md"), "w", encoding="utf-8") as f:
            f.write(cache_whitelist_md)
        print(f"  -> build/{platform}/cache/WHITELIST.md")

        # 4. Cache FPC
        cache_fpc_md = build_cache_fpc(profile)
        with open(os.path.join(dest_cache, "FPC.md"), "w", encoding="utf-8") as f:
            f.write(cache_fpc_md)
        print(f"  -> build/{platform}/cache/FPC.md")

    print("\nAll profiles successfully compiled!")


if __name__ == "__main__":
    main()
