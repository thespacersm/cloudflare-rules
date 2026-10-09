# Backup regole Cloudflare - anticaenotecagiulianelli.com

Zona: `anticaenotecagiulianelli.com` (`d7a0443dab4ffc36ee4a63f51fe67d58`) - piano Free  
Backup del: 2026-10-09 09:27 UTC  
Stato letto live prima di applicare il WAF del profilo WooCommerce (con catchr). La cache non viene toccata dal deploy.

## WAF custom (`http_request_firewall_custom`)

Ruleset `85c2549f2e5c4b0696364854453859e8` - versione 2 - ultimo aggiornamento 2026-09-01T14:40:27.815536Z

### 1. WHITELIST

- ID regola: `a60eb3d6d76a4f7abac58ae3232a13b1`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_ratelimit", "http_request_firewall_managed", "http_request_sbfm"], "products": ["bic", "zoneLockdown", "rateLimit", "waf", "securityLevel", "hot", "uaBlock"], "ruleset": "current"}`

Espressione:
```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (http.user_agent contains "DaneaEasyfatt") or (http.request.uri.path contains "M2ePro") or (cf.client.bot and http.user_agent contains "bingbot") or (http.request.uri.path contains "paypal") or (http.request.uri.path contains "bkn") or (http.request.uri.path contains "stripe") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "woo-feed") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma")
```

### 2. BLOCCO NAZIONI

- ID regola: `00e3b642cae0400ca99557b67aee0cd5`
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
    "expression": "(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains \"Java\" and ip.src.country eq \"IT\") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains \"Google\") or (http.user_agent contains \"DaneaEasyfatt\") or (http.request.uri.path contains \"M2ePro\") or (cf.client.bot and http.user_agent contains \"bingbot\") or (http.request.uri.path contains \"paypal\") or (http.request.uri.path contains \"bkn\") or (http.request.uri.path contains \"stripe\") or (http.request.uri.path contains \"doofinder\") or (http.request.uri.path contains \"trovaprezzi\") or (http.request.uri.path contains \"woo-feed\") or (ip.src eq 49.12.69.209 and http.user_agent contains \"Kuma\")",
    "id": "a60eb3d6d76a4f7abac58ae3232a13b1",
    "last_updated": "2026-09-01T14:40:27.815536Z",
    "logging": {
      "enabled": true
    },
    "ref": "a60eb3d6d76a4f7abac58ae3232a13b1",
    "version": "1"
  },
  {
    "action": "managed_challenge",
    "description": "BLOCCO NAZIONI",
    "enabled": true,
    "expression": "(not ip.src.country in {\"IT\" \"SM\" \"VA\"})",
    "id": "00e3b642cae0400ca99557b67aee0cd5",
    "last_updated": "2026-09-01T14:40:27.815536Z",
    "ref": "00e3b642cae0400ca99557b67aee0cd5",
    "version": "1"
  }
]
```
</details>

## Cache rules (non toccata) (`http_request_cache_settings`)

Ruleset `9202f4417a784c29af7095cae0c6446b` - versione 1 - ultimo aggiornamento 2026-09-14T06:55:58.649323Z

### 1. WordPress FPC - Cache All except Backoffice and API

- ID regola: `287c66f3131245db954c6c3f9167090d`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"browser_ttl": {"mode": "respect_origin"}, "cache": true, "edge_ttl": {"default": 14400, "mode": "override_origin"}, "respect_strong_etags": true}`

Espressione:
```text
(http.request.method in {"GET" "HEAD"} and not starts_with(http.request.uri.path, "/wp-admin") and not starts_with(http.request.uri.path, "/wp-json") and not http.request.uri.path contains "wp-login.php" and not http.request.uri.path contains "xmlrpc.php" and not http.request.uri.path contains "wp-cron.php" and not http.request.uri.query contains "rest_route=" and not http.request.uri.query contains "preview=true" and not http.cookie contains "wordpress_logged_in" and not http.cookie contains "comment_author" and not http.cookie contains "wp-postpass_" and not http.cookie contains "woocommerce_items_in_cart")
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
      "edge_ttl": {
        "default": 14400,
        "mode": "override_origin"
      },
      "respect_strong_etags": true
    },
    "description": "WordPress FPC - Cache All except Backoffice and API",
    "enabled": true,
    "expression": "(http.request.method in {\"GET\" \"HEAD\"} and not starts_with(http.request.uri.path, \"/wp-admin\") and not starts_with(http.request.uri.path, \"/wp-json\") and not http.request.uri.path contains \"wp-login.php\" and not http.request.uri.path contains \"xmlrpc.php\" and not http.request.uri.path contains \"wp-cron.php\" and not http.request.uri.query contains \"rest_route=\" and not http.request.uri.query contains \"preview=true\" and not http.cookie contains \"wordpress_logged_in\" and not http.cookie contains \"comment_author\" and not http.cookie contains \"wp-postpass_\" and not http.cookie contains \"woocommerce_items_in_cart\")",
    "id": "287c66f3131245db954c6c3f9167090d",
    "last_updated": "2026-09-14T06:55:58.649323Z",
    "ref": "287c66f3131245db954c6c3f9167090d",
    "version": "1"
  }
]
```
</details>

## Rate limiting (`http_ratelimit`)

_Nessun ruleset._
