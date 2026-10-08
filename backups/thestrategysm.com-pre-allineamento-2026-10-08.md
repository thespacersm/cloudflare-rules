# Backup regole Cloudflare - thestrategysm.com

Zona: `thestrategysm.com` (`03d87d90fc2bfa8f7729ca150970d038`)  
Backup del: 2026-10-08 12:16 UTC  
Stato letto live prima di allineare cache (static) e applicare il profilo WordPress (WAF).

## WAF custom (`http_request_firewall_custom`)

Ruleset `b036c2cf5c764cdf8859a7cde8736737` - versione 4 - ultimo aggiornamento 2026-08-05T12:24:45.105369Z

### 1. Blocco xmlrpc.php

- ID regola: `af7dd889e68d4cc484357c405b6786ff`
- Azione: `block`
- Attiva: `False`

Espressione:
```text
(http.request.uri.path eq "/xmlrpc.php")
```

### 2. Blocco Asia-Africa

- ID regola: `fff4b3088b984fe9937a43bc42a622bf`
- Azione: `block`
- Attiva: `False`

Espressione:
```text
(ip.src.continent eq "AS") or (ip.src.continent eq "AF")
```

<details><summary>JSON completo</summary>

```json
[
  {
    "action": "block",
    "description": "Blocco xmlrpc.php",
    "enabled": false,
    "expression": "(http.request.uri.path eq \"/xmlrpc.php\")",
    "id": "af7dd889e68d4cc484357c405b6786ff",
    "last_updated": "2026-08-05T12:24:42.836035Z",
    "ref": "af7dd889e68d4cc484357c405b6786ff",
    "version": "2"
  },
  {
    "action": "block",
    "description": "Blocco Asia-Africa",
    "enabled": false,
    "expression": "(ip.src.continent eq \"AS\") or (ip.src.continent eq \"AF\")",
    "id": "fff4b3088b984fe9937a43bc42a622bf",
    "last_updated": "2026-08-05T12:24:45.105369Z",
    "ref": "fff4b3088b984fe9937a43bc42a622bf",
    "version": "2"
  }
]
```
</details>

## Cache rules (`http_request_cache_settings`)

Ruleset `833c45df454b4744a685317c4974e7b0` - versione 2 - ultimo aggiornamento 2026-10-08T10:50:12.249727Z

### 1. FULL PAGE CACHE (FPC) - WORDPRESS [STATIC]

- ID regola: `38707c5aeb544cfeb081e3e77b512c1f`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"browser_ttl": {"mode": "respect_origin"}, "cache": true, "cache_key": {"custom_key": {"query_string": {"exclude": {"all": true}}}}, "edge_ttl": {"default": 2678400, "mode": "override_origin", "status_code_ttl": [{"status_code_range": {"from": 500, "to": 526}, "value": -1}, {"status_code_range": {"from": 400, "to": 499}, "value": 300}]}}`

Espressione:
```text
http.request.method in {"GET" "HEAD"}
```

### 2. CACHE WHITELIST (BYPASS) - WORDPRESS

- ID regola: `e359897973db4c27a558b7602ef0562f`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": false}`

Espressione:
```text
(http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login") or (http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php") or ((http.cookie contains "wordpress_logged_in_") and not http.request.uri.path.extension in {"css" "js" "jpg" "jpeg" "png" "gif" "webp" "avif" "svg" "ico" "bmp" "tif" "tiff" "woff" "woff2" "ttf" "otf" "eot"}) or ((http.cookie contains "comment_author_") and not http.request.uri.path.extension in {"css" "js" "jpg" "jpeg" "png" "gif" "webp" "avif" "svg" "ico" "bmp" "tif" "tiff" "woff" "woff2" "ttf" "otf" "eot"}) or (http.request.uri.path contains "/ts_proxy.php") or (http.request.uri.path contains "/proxy.php")
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
        "default": 2678400,
        "mode": "override_origin",
        "status_code_ttl": [
          {
            "status_code_range": {
              "from": 500,
              "to": 526
            },
            "value": -1
          },
          {
            "status_code_range": {
              "from": 400,
              "to": 499
            },
            "value": 300
          }
        ]
      }
    },
    "description": "FULL PAGE CACHE (FPC) - WORDPRESS [STATIC]",
    "enabled": true,
    "expression": "http.request.method in {\"GET\" \"HEAD\"}",
    "id": "38707c5aeb544cfeb081e3e77b512c1f",
    "last_updated": "2026-10-08T10:49:18.657493Z",
    "ref": "38707c5aeb544cfeb081e3e77b512c1f",
    "version": "1"
  },
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": false
    },
    "description": "CACHE WHITELIST (BYPASS) - WORDPRESS",
    "enabled": true,
    "expression": "(http.request.uri.path contains \"/wp-admin\" or http.request.uri.path contains \"/wp-login\") or (http.request.uri.path contains \"/wp-json\" or http.request.uri.path contains \"/xmlrpc.php\") or ((http.cookie contains \"wordpress_logged_in_\") and not http.request.uri.path.extension in {\"css\" \"js\" \"jpg\" \"jpeg\" \"png\" \"gif\" \"webp\" \"avif\" \"svg\" \"ico\" \"bmp\" \"tif\" \"tiff\" \"woff\" \"woff2\" \"ttf\" \"otf\" \"eot\"}) or ((http.cookie contains \"comment_author_\") and not http.request.uri.path.extension in {\"css\" \"js\" \"jpg\" \"jpeg\" \"png\" \"gif\" \"webp\" \"avif\" \"svg\" \"ico\" \"bmp\" \"tif\" \"tiff\" \"woff\" \"woff2\" \"ttf\" \"otf\" \"eot\"}) or (http.request.uri.path contains \"/ts_proxy.php\") or (http.request.uri.path contains \"/proxy.php\")",
    "id": "e359897973db4c27a558b7602ef0562f",
    "last_updated": "2026-10-08T10:50:12.249727Z",
    "ref": "e359897973db4c27a558b7602ef0562f",
    "version": "1"
  }
]
```
</details>
