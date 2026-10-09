# Backup regole Cloudflare - kissrimini.com

Zona: `kissrimini.com` (`489641e4d84918895c38abe8d2ec46db`) - piano Free  
Backup del: 2026-10-09 07:32 UTC  
Stato letto live prima di applicare il WAF del profilo WooCommerce. La cache non viene toccata dal deploy.

## WAF custom (`http_request_firewall_custom`)

Ruleset `c11d288b278a4a1aad58df32d88b78a7` - versione 4 - ultimo aggiornamento 2026-08-04T09:39:38.206554Z

### 1. CONDIZIONE

- ID regola: `37f8924c15a3442e90baa823b75dc82b`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_request_sbfm"]}`

Espressione:
```text
(http.request.uri contains "/wp-admin")
```

### 2. WooCommerce - Allow Essential Paths

- ID regola: `5c31176d829c4fd68d2182599981f768`
- Azione: `skip`
- Attiva: `True`
- Parametri: `{"phases": ["http_request_sbfm"]}`

Espressione:
```text
(http.request.uri contains "/cart") or (http.request.uri contains "URI contains /checkout") or (http.request.uri contains "URI contains /my-account")
```

<details><summary>JSON completo</summary>

```json
[
  {
    "action": "skip",
    "action_parameters": {
      "phases": [
        "http_request_sbfm"
      ]
    },
    "description": "CONDIZIONE",
    "enabled": true,
    "expression": "(http.request.uri contains \"/wp-admin\")",
    "id": "37f8924c15a3442e90baa823b75dc82b",
    "last_updated": "2025-11-17T17:48:41.417976Z",
    "logging": {
      "enabled": true
    },
    "ref": "37f8924c15a3442e90baa823b75dc82b",
    "version": "1"
  },
  {
    "action": "skip",
    "action_parameters": {
      "phases": [
        "http_request_sbfm"
      ]
    },
    "description": "WooCommerce - Allow Essential Paths",
    "enabled": true,
    "expression": "(http.request.uri contains \"/cart\") or (http.request.uri contains \"URI contains /checkout\") or (http.request.uri contains \"URI contains /my-account\")",
    "id": "5c31176d829c4fd68d2182599981f768",
    "last_updated": "2026-08-04T09:39:38.206554Z",
    "logging": {
      "enabled": true
    },
    "ref": "5c31176d829c4fd68d2182599981f768",
    "version": "3"
  }
]
```
</details>

## Cache rules (non toccata) (`http_request_cache_settings`)

Ruleset `54dd2f9de41a44f0a94cf6f59251d449` - versione 11 - ultimo aggiornamento 2026-04-11T21:24:30.43571Z

### 1. No Cache cart

- ID regola: `564ceec46a9e4d9d987fae58a48efe4f`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": false}`

Espressione:
```text
(http.request.uri.path contains "/cart")
```

### 2. checkout

- ID regola: `cd587e98c0c6425a8178dcefcd7e70b7`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": false}`

Espressione:
```text
(http.request.uri contains "/checkout")
```

### 3. my-account

- ID regola: `b7a1cfd99cdd45bd8bad6fb5168a8a71`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": false}`

Espressione:
```text
(http.request.uri contains "/my-account")
```

### 4. CACHE IMMAGINI

- ID regola: `a71ca6d0c106403e98abe17e52219e2c`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": true, "edge_ttl": {"default": 2678400, "mode": "override_origin"}}`

Espressione:
```text
(http.request.uri contains "/wp-content/uploads/")
```

### 5. HOME SAFE CACHE

- ID regola: `a6fd3fc4dd944743b8622d7b076ad045`
- Azione: `set_cache_settings`
- Attiva: `True`
- Parametri: `{"cache": false}`

Espressione:
```text
(http.request.uri.path eq "/")
```

<details><summary>JSON completo</summary>

```json
[
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": false
    },
    "description": "No Cache cart",
    "enabled": true,
    "expression": "(http.request.uri.path contains \"/cart\")",
    "id": "564ceec46a9e4d9d987fae58a48efe4f",
    "last_updated": "2026-04-05T18:44:14.202867Z",
    "ref": "564ceec46a9e4d9d987fae58a48efe4f",
    "version": "2"
  },
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": false
    },
    "description": "checkout",
    "enabled": true,
    "expression": "(http.request.uri contains \"/checkout\")",
    "id": "cd587e98c0c6425a8178dcefcd7e70b7",
    "last_updated": "2026-04-05T18:43:51.280027Z",
    "ref": "cd587e98c0c6425a8178dcefcd7e70b7",
    "version": "1"
  },
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": false
    },
    "description": "my-account",
    "enabled": true,
    "expression": "(http.request.uri contains \"/my-account\")",
    "id": "b7a1cfd99cdd45bd8bad6fb5168a8a71",
    "last_updated": "2026-04-05T18:45:25.01397Z",
    "ref": "b7a1cfd99cdd45bd8bad6fb5168a8a71",
    "version": "1"
  },
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": true,
      "edge_ttl": {
        "default": 2678400,
        "mode": "override_origin"
      }
    },
    "description": "CACHE IMMAGINI",
    "enabled": true,
    "expression": "(http.request.uri contains \"/wp-content/uploads/\")",
    "id": "a71ca6d0c106403e98abe17e52219e2c",
    "last_updated": "2026-04-05T19:50:26.142273Z",
    "ref": "a71ca6d0c106403e98abe17e52219e2c",
    "version": "1"
  },
  {
    "action": "set_cache_settings",
    "action_parameters": {
      "cache": false
    },
    "description": "HOME SAFE CACHE",
    "enabled": true,
    "expression": "(http.request.uri.path eq \"/\")",
    "id": "a6fd3fc4dd944743b8622d7b076ad045",
    "last_updated": "2026-04-11T16:39:20.429096Z",
    "ref": "a6fd3fc4dd944743b8622d7b076ad045",
    "version": "1"
  }
]
```
</details>

## Rate limiting (`http_ratelimit`)

_Nessun ruleset._
