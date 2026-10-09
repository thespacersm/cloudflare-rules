# Backup regole Cloudflare - gioiellitamburini.com

Zona: `gioiellitamburini.com` (`95b16598bc21b46ed835dc6018161198`) - piano Free  
Backup del: 2026-10-09 07:28 UTC  
Stato letto live prima di applicare il profilo WooCommerce (WAF).

## WAF custom (`http_request_firewall_custom`)

Ruleset `b44f5388b57f45e09120cfc6399f7ab6` - versione 1 - ultimo aggiornamento 2026-09-04T09:42:16.695687Z

### 1. WHITELIST

- ID regola: `ec4e77aab07344f580b7dd0dda2ad53c`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_ratelimit", "http_request_firewall_managed", "http_request_sbfm"], "products": ["bic", "zoneLockdown", "rateLimit", "waf", "securityLevel", "hot", "uaBlock"], "ruleset": "current"}`

Espressione:
```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (http.user_agent contains "DaneaEasyfatt") or (http.request.uri.path contains "M2ePro") or (cf.client.bot and http.user_agent contains "bingbot") or (http.request.uri.path contains "paypal") or (http.request.uri.path contains "bkn") or (http.request.uri.path contains "stripe") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "woo-feed") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (http.request.uri.path contains ".jpg") or (http.request.uri.path contains ".jpeg") or (http.request.uri.path contains ".png") or (http.request.uri.path contains ".webp") or (http.request.uri.path contains ".gif") or (http.request.uri.path contains ".svg") or (http.request.uri.path contains ".ico") or (http.request.uri.path contains ".avif") or (http.request.uri.path contains ".bmp") or (http.request.uri.path contains ".tif") or (http.request.uri.path contains ".tiff")
```

### 2. BLOCCO NAZIONI

- ID regola: `50f5d68d908c4b2a89683c96a673607d`
- Azione: `managed_challenge`
- Attiva: `True`

Espressione:
```text
(not ip.src.country in {"IT" "SM" "VA"})
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
    "description": "WHITELIST",
    "enabled": true,
    "expression": "(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains \"Java\" and ip.src.country eq \"IT\") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains \"Google\") or (http.user_agent contains \"DaneaEasyfatt\") or (http.request.uri.path contains \"M2ePro\") or (cf.client.bot and http.user_agent contains \"bingbot\") or (http.request.uri.path contains \"paypal\") or (http.request.uri.path contains \"bkn\") or (http.request.uri.path contains \"stripe\") or (http.request.uri.path contains \"doofinder\") or (http.request.uri.path contains \"trovaprezzi\") or (http.request.uri.path contains \"woo-feed\") or (ip.src eq 49.12.69.209 and http.user_agent contains \"Kuma\") or (http.request.uri.path contains \".jpg\") or (http.request.uri.path contains \".jpeg\") or (http.request.uri.path contains \".png\") or (http.request.uri.path contains \".webp\") or (http.request.uri.path contains \".gif\") or (http.request.uri.path contains \".svg\") or (http.request.uri.path contains \".ico\") or (http.request.uri.path contains \".avif\") or (http.request.uri.path contains \".bmp\") or (http.request.uri.path contains \".tif\") or (http.request.uri.path contains \".tiff\")",
    "id": "ec4e77aab07344f580b7dd0dda2ad53c",
    "last_updated": "2026-09-04T09:42:16.695687Z",
    "logging": {
      "enabled": true
    },
    "ref": "ec4e77aab07344f580b7dd0dda2ad53c",
    "version": "1"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO NAZIONI",
    "enabled": true,
    "expression": "(not ip.src.country in {\"IT\" \"SM\" \"VA\"})",
    "id": "50f5d68d908c4b2a89683c96a673607d",
    "last_updated": "2026-09-04T09:42:16.695687Z",
    "ref": "50f5d68d908c4b2a89683c96a673607d",
    "version": "1"
  }
]
```
</details>

## Rate limiting (`http_ratelimit`)

_Nessun ruleset._

## Cache rules (`http_request_cache_settings`)

_Nessun ruleset._
