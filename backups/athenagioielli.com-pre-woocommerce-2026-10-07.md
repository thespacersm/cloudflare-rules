# Backup regole Cloudflare - athenagioielli.com

Zona: `athenagioielli.com` (`23ab32312722b25c9418bd5333d63706`)  
Backup del: 2026-10-07 08:53 UTC  
Stato letto live prima del deploy del profilo WooCommerce (WAF).

## WAF custom (`http_request_firewall_custom`)

Ruleset `17092bdc016d401bb28ac7de07c8d5a9` - versione 21 - ultimo aggiornamento 2026-08-28T11:02:46.162824Z

### 1. WHITELIST

- ID regola: `1eb96703b79144fcbdfd3485e6419ed7`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_ratelimit", "http_request_firewall_managed", "http_request_sbfm"], "products": ["zoneLockdown", "uaBlock", "bic", "hot", "securityLevel", "rateLimit", "waf"], "ruleset": "current"}`

Espressione:
```text
(http.request.uri.path contains "woo-feed")
```

### 2. Regola per mitigare Gtranslate.io

- ID regola: `f808d45c617444e1834ec8b115c83f61`
- Azione: `js_challenge`
- Attiva: `False`

Espressione:
```text
ip.src eq 147.135.170.82
```

### 3. BLOCCO FACEBOOK

- ID regola: `15e4cef0fffc41e3bad6ed0bf61d154e`
- Azione: `managed_challenge`
- Attiva: `True`

Espressione:
```text
(http.user_agent contains "meta-externalagent") or (http.user_agent contains "facebookexternalhit") or (http.user_agent contains "meta-externalads")
```

### 4. BLOCCO USA (NON GOOGLE)

- ID regola: `400a18bde76547438955179f73ea659f`
- Azione: `managed_challenge`
- Attiva: `True`

Espressione:
```text
(ip.src.country eq "US" and not http.user_agent contains "google" and not http.user_agent contains "bingbot" and not http.user_agent contains "WordPress" and not http.user_agent contains "Google")

```

### 5. BLOCCO NAZIONI

- ID regola: `6d9edf51114e44918e0ceb156e19c360`
- Azione: `managed_challenge`
- Attiva: `True`

Espressione:
```text
(not ip.src.country in {"AT" "BE" "FI" "FR" "DE" "GR" "HU" "IE" "IT" "LU" "NL" "NO" "PT" "SM" "SK" "SI" "ES" "SE" "CH" "GB" "US" "VA"})
```

<details><summary>JSON completo</summary>

```json
[
  {
    "action": "skip",
    "action_parameters": {
      "phases": [
        "http_ratelimit",
        "http_request_firewall_managed",
        "http_request_sbfm"
      ],
      "products": [
        "zoneLockdown",
        "uaBlock",
        "bic",
        "hot",
        "securityLevel",
        "rateLimit",
        "waf"
      ],
      "ruleset": "current"
    },
    "description": "WHITELIST",
    "enabled": true,
    "expression": "(http.request.uri.path contains \"woo-feed\")",
    "id": "1eb96703b79144fcbdfd3485e6419ed7",
    "last_updated": "2026-08-28T11:02:46.162824Z",
    "logging": {
      "enabled": true
    },
    "ref": "1eb96703b79144fcbdfd3485e6419ed7",
    "version": "3"
  },
  {
    "action": "js_challenge",
    "description": "Regola per mitigare Gtranslate.io",
    "enabled": false,
    "expression": "ip.src eq 147.135.170.82",
    "id": "f808d45c617444e1834ec8b115c83f61",
    "last_updated": "2026-05-08T10:15:39.165001Z",
    "ref": "f808d45c617444e1834ec8b115c83f61",
    "version": "4"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO FACEBOOK",
    "enabled": true,
    "expression": "(http.user_agent contains \"meta-externalagent\") or (http.user_agent contains \"facebookexternalhit\") or (http.user_agent contains \"meta-externalads\")",
    "id": "15e4cef0fffc41e3bad6ed0bf61d154e",
    "last_updated": "2026-08-28T11:02:14.39031Z",
    "ref": "15e4cef0fffc41e3bad6ed0bf61d154e",
    "version": "4"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO USA (NON GOOGLE)",
    "enabled": true,
    "expression": "(ip.src.country eq \"US\" and not http.user_agent contains \"google\" and not http.user_agent contains \"bingbot\" and not http.user_agent contains \"WordPress\" and not http.user_agent contains \"Google\")\n",
    "id": "400a18bde76547438955179f73ea659f",
    "last_updated": "2026-07-23T10:02:35.250707Z",
    "ref": "400a18bde76547438955179f73ea659f",
    "version": "1"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO NAZIONI",
    "enabled": true,
    "expression": "(not ip.src.country in {\"AT\" \"BE\" \"FI\" \"FR\" \"DE\" \"GR\" \"HU\" \"IE\" \"IT\" \"LU\" \"NL\" \"NO\" \"PT\" \"SM\" \"SK\" \"SI\" \"ES\" \"SE\" \"CH\" \"GB\" \"US\" \"VA\"})",
    "id": "6d9edf51114e44918e0ceb156e19c360",
    "last_updated": "2026-07-23T10:11:27.400122Z",
    "ref": "6d9edf51114e44918e0ceb156e19c360",
    "version": "1"
  }
]
```
</details>

## Cache rules (`http_request_cache_settings`)

_Nessun ruleset._
