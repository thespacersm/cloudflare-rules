# Backup regole Cloudflare - natumparfum.com

Zona: `natumparfum.com` (`39fd2295e99a170bc1dde3c528d725f0`) - piano Free  
Backup del: 2026-10-09 08:20 UTC  
Stato letto live prima di applicare il profilo WordPress (WAF).

## WAF custom (`http_request_firewall_custom`)

Ruleset `0ef4ad2077fb43edb170886c58b498fa` - versione 1 - ultimo aggiornamento 2026-09-04T08:50:29.554884Z

### 1. WHITELIST

- ID regola: `efd34e5cceae4bc7bbb0cfa6d7f87500`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_ratelimit", "http_request_firewall_managed", "http_request_sbfm"], "products": ["bic", "zoneLockdown", "rateLimit", "waf", "securityLevel", "hot", "uaBlock"], "ruleset": "current"}`

Espressione:
```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (http.user_agent contains "DaneaEasyfatt") or (http.request.uri.path contains "M2ePro") or (cf.client.bot and http.user_agent contains "bingbot") or (http.request.uri.path contains "paypal") or (http.request.uri.path contains "bkn") or (http.request.uri.path contains "stripe") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "woo-feed") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (http.request.uri.path contains ".jpg") or (http.request.uri.path contains ".jpeg") or (http.request.uri.path contains ".png") or (http.request.uri.path contains ".webp") or (http.request.uri.path contains ".gif") or (http.request.uri.path contains ".svg") or (http.request.uri.path contains ".ico") or (http.request.uri.path contains ".avif") or (http.request.uri.path contains ".bmp") or (http.request.uri.path contains ".tif") or (http.request.uri.path contains ".tiff")
```

### 2. BLOCCO NAZIONI

- ID regola: `f1a29ff1768249eaabf83a5a8dae982b`
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
    "id": "efd34e5cceae4bc7bbb0cfa6d7f87500",
    "last_updated": "2026-09-04T08:50:29.554884Z",
    "logging": {
      "enabled": true
    },
    "ref": "efd34e5cceae4bc7bbb0cfa6d7f87500",
    "version": "1"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO NAZIONI",
    "enabled": true,
    "expression": "(not ip.src.country in {\"IT\" \"SM\" \"VA\"})",
    "id": "f1a29ff1768249eaabf83a5a8dae982b",
    "last_updated": "2026-09-04T08:50:29.554884Z",
    "ref": "f1a29ff1768249eaabf83a5a8dae982b",
    "version": "1"
  }
]
```
</details>

## Rate limiting (`http_ratelimit`)

_Nessun ruleset._

## Cache rules (`http_request_cache_settings`)

_Nessun ruleset._
