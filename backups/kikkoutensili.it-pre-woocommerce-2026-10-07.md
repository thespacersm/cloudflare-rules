# Backup regole Cloudflare - kikkoutensili.it

Zona: `kikkoutensili.it` (`2b070f3c9c6d131b7dc7d83d2c8c4025`)  
Backup del: 2026-10-07 08:38 UTC  
Stato letto live dall'API prima del deploy del profilo WooCommerce (WAF).

## WAF custom (`http_request_firewall_custom`)

Ruleset `05ab74cf653346998979a057d1a82869` - versione 92 - ultimo aggiornamento 2026-10-06T14:32:06.335888Z

### 1. Sync / API - eShoppingAdvisor

- ID regola: `8921285937e8455da0eed0d8957734f2`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_request_firewall_managed", "http_ratelimit", "http_request_sbfm"], "ruleset": "current"}`

Espressione:
```text
http.user_agent contains "EsaCmsApiIntegrations" and ip.src in {204.168.128.0/17} and starts_with(http.request.uri.path, "/wp-json/wc/")
```

### 2. WHITELIST

- ID regola: `ccdd38c7f449458db219c5290352cbb1`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_ratelimit", "http_request_firewall_managed", "http_request_sbfm"], "products": ["bic", "zoneLockdown", "rateLimit", "waf", "securityLevel", "hot", "uaBlock"], "ruleset": "current"}`

Espressione:
```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (http.user_agent contains "DaneaEasyfatt") or (http.request.uri.path contains "M2ePro") or (cf.client.bot and http.user_agent contains "bingbot") or (http.request.uri.path contains "paypal") or (http.request.uri.path contains "bkn") or (http.request.uri.path contains "stripe") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "woo-feed") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (http.request.uri.path contains "/wp-json/space/v1/products") or (ip.src eq 51.210.33.22) or (ip.src eq 51.75.189.227) or (ip.src.asnum eq 16276) or (ip.src in {185.107.232.0/24 1.179.112.0/24 89.186.51.31}) or (http.user_agent contains "SPRIX") or (ip.src in {34.246.194.207 34.240.30.93 54.171.95.188 52.49.117.159 52.215.188.32 3.249.68.14 54.246.152.94 3.250.54.94 188.13.93.38 5.249.157.200}) or (ip.src in {5.39.1.224/27 5.39.109.160/27 15.235.27.0/24 15.235.96.0/24 15.235.98.0/24 37.59.204.128/27 51.68.247.192/27 51.75.236.128/27 51.89.129.0/24 51.161.37.0/24 51.161.65.0/24 51.195.183.0/24 51.195.215.0/24 51.195.244.0/24 51.222.95.0/24 51.222.168.0/24 51.222.253.0/26 54.36.148.0/24 54.36.149.0/24 54.37.118.64/27 54.38.147.0/24 54.39.0.0/24 54.39.6.0/24 54.39.89.0/24 54.39.136.0/24 54.39.203.0/24 54.39.210.0/24 92.222.104.192/27 92.222.108.96/27 94.23.188.192/27 142.44.220.0/24 142.44.225.0/24 142.44.228.0/24 142.44.233.0/24 148.113.128.0/24 148.113.130.0/24 168.100.149.0/24 167.114.139.0/24 176.31.139.0/27 198.244.168.0/24 198.244.183.0/24 198.244.226.0/24 198.244.240.0/24 198.244.242.0/24 202.8.40.0/22 198.244.186.193 198.244.186.194 198.244.186.195 198.244.186.196 198.244.186.197 198.244.186.198 198.244.186.199 198.244.186.200 198.244.186.201 198.244.186.202 202.94.84.110 202.94.84.111 202.94.84.112 202.94.84.113}) or (http.request.uri.path contains "wpwoof-feed") or (ends_with(http.request.uri.path, ".jpg")) or (ends_with(http.request.uri.path, ".jpeg")) or (ends_with(http.request.uri.path, ".png")) or (ends_with(http.request.uri.path, ".webp")) or (ends_with(http.request.uri.path, ".gif")) or (ends_with(http.request.uri.path, ".svg")) or (ends_with(http.request.uri.path, ".ico")) or (ends_with(http.request.uri.path, ".avif")) or (ends_with(http.request.uri.path, ".bmp")) or (ends_with(http.request.uri.path, ".tif")) or (ends_with(http.request.uri.path, ".tiff")) or (http.request.uri.path contains "/fb") or (cf.client.bot and http.user_agent contains "facebook") or (cf.client.bot and http.user_agent contains "meta")
```

### 3. BLOCCO NAZIONI

- ID regola: `6dec1b5dc8d1420b8f6b6454a06fcfd1`
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
        "http_request_firewall_managed",
        "http_ratelimit",
        "http_request_sbfm"
      ],
      "ruleset": "current"
    },
    "description": "Sync / API - eShoppingAdvisor",
    "enabled": true,
    "expression": "http.user_agent contains \"EsaCmsApiIntegrations\" and ip.src in {204.168.128.0/17} and starts_with(http.request.uri.path, \"/wp-json/wc/\")",
    "id": "8921285937e8455da0eed0d8957734f2",
    "last_updated": "2026-10-06T14:32:06.335888Z",
    "logging": {
      "enabled": true
    },
    "ref": "8921285937e8455da0eed0d8957734f2",
    "version": "2"
  },
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
    "expression": "(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains \"Java\" and ip.src.country eq \"IT\") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains \"Google\") or (http.user_agent contains \"DaneaEasyfatt\") or (http.request.uri.path contains \"M2ePro\") or (cf.client.bot and http.user_agent contains \"bingbot\") or (http.request.uri.path contains \"paypal\") or (http.request.uri.path contains \"bkn\") or (http.request.uri.path contains \"stripe\") or (http.request.uri.path contains \"doofinder\") or (http.request.uri.path contains \"trovaprezzi\") or (http.request.uri.path contains \"woo-feed\") or (ip.src eq 49.12.69.209 and http.user_agent contains \"Kuma\") or (http.request.uri.path contains \"/wp-json/space/v1/products\") or (ip.src eq 51.210.33.22) or (ip.src eq 51.75.189.227) or (ip.src.asnum eq 16276) or (ip.src in {185.107.232.0/24 1.179.112.0/24 89.186.51.31}) or (http.user_agent contains \"SPRIX\") or (ip.src in {34.246.194.207 34.240.30.93 54.171.95.188 52.49.117.159 52.215.188.32 3.249.68.14 54.246.152.94 3.250.54.94 188.13.93.38 5.249.157.200}) or (ip.src in {5.39.1.224/27 5.39.109.160/27 15.235.27.0/24 15.235.96.0/24 15.235.98.0/24 37.59.204.128/27 51.68.247.192/27 51.75.236.128/27 51.89.129.0/24 51.161.37.0/24 51.161.65.0/24 51.195.183.0/24 51.195.215.0/24 51.195.244.0/24 51.222.95.0/24 51.222.168.0/24 51.222.253.0/26 54.36.148.0/24 54.36.149.0/24 54.37.118.64/27 54.38.147.0/24 54.39.0.0/24 54.39.6.0/24 54.39.89.0/24 54.39.136.0/24 54.39.203.0/24 54.39.210.0/24 92.222.104.192/27 92.222.108.96/27 94.23.188.192/27 142.44.220.0/24 142.44.225.0/24 142.44.228.0/24 142.44.233.0/24 148.113.128.0/24 148.113.130.0/24 168.100.149.0/24 167.114.139.0/24 176.31.139.0/27 198.244.168.0/24 198.244.183.0/24 198.244.226.0/24 198.244.240.0/24 198.244.242.0/24 202.8.40.0/22 198.244.186.193 198.244.186.194 198.244.186.195 198.244.186.196 198.244.186.197 198.244.186.198 198.244.186.199 198.244.186.200 198.244.186.201 198.244.186.202 202.94.84.110 202.94.84.111 202.94.84.112 202.94.84.113}) or (http.request.uri.path contains \"wpwoof-feed\") or (ends_with(http.request.uri.path, \".jpg\")) or (ends_with(http.request.uri.path, \".jpeg\")) or (ends_with(http.request.uri.path, \".png\")) or (ends_with(http.request.uri.path, \".webp\")) or (ends_with(http.request.uri.path, \".gif\")) or (ends_with(http.request.uri.path, \".svg\")) or (ends_with(http.request.uri.path, \".ico\")) or (ends_with(http.request.uri.path, \".avif\")) or (ends_with(http.request.uri.path, \".bmp\")) or (ends_with(http.request.uri.path, \".tif\")) or (ends_with(http.request.uri.path, \".tiff\")) or (http.request.uri.path contains \"/fb\") or (cf.client.bot and http.user_agent contains \"facebook\") or (cf.client.bot and http.user_agent contains \"meta\")",
    "id": "ccdd38c7f449458db219c5290352cbb1",
    "last_updated": "2026-09-04T12:44:27.873827Z",
    "logging": {
      "enabled": true
    },
    "ref": "ccdd38c7f449458db219c5290352cbb1",
    "version": "7"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO NAZIONI",
    "enabled": true,
    "expression": "(not ip.src.country in {\"IT\" \"SM\" \"VA\"})",
    "id": "6dec1b5dc8d1420b8f6b6454a06fcfd1",
    "last_updated": "2026-09-04T08:21:53.081911Z",
    "ref": "6dec1b5dc8d1420b8f6b6454a06fcfd1",
    "version": "1"
  }
]
```
</details>

## Cache rules (`http_request_cache_settings`)

Ruleset `dd9f4438628746f1a788753b1ec289a6` - versione 8 - ultimo aggiornamento 2026-09-28T06:46:43.939114Z

### 1. fbguard - cache edge delle risposte per scraper Meta

- ID regola: `93e54135521d40cabf77ae7e08c4b28a`
- Azione: `set_cache_settings`
- Attiva: `False`
- Parametri: `{"browser_ttl": {"mode": "respect_origin"}, "cache": true, "cache_key": {"custom_key": {"query_string": {"exclude": {"all": true}}}}, "edge_ttl": {"mode": "respect_origin"}}`

Espressione:
```text
(http.request.uri.path contains "/__fbguard")
```

<details><summary>JSON completo</summary>

```json
[
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "browser_ttl": {
        "mode": "respect_origin"
      },
      "cache": true,
      "cache_key": {
        "custom_key": {
          "query_string": {
            "exclude": {
              "all": true
            }
          }
        }
      },
      "edge_ttl": {
        "mode": "respect_origin"
      }
    },
    "description": "fbguard - cache edge delle risposte per scraper Meta",
    "enabled": false,
    "expression": "(http.request.uri.path contains \"/__fbguard\")",
    "id": "93e54135521d40cabf77ae7e08c4b28a",
    "last_updated": "2026-09-28T06:46:43.939114Z",
    "ref": "93e54135521d40cabf77ae7e08c4b28a",
    "version": "2"
  }
]
```
</details>
