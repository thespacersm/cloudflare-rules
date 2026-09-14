# FULL PAGE CACHE (FPC) - MAGENTO 2

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare per velocizzare al massimo la navigazione su **Magento 2** (pagine catalogo, schede prodotto, landing page, categorie).

### Posizione nella Ruleset
Deve trovarsi **dopo** la regola di Cache Whitelist (Bypass).

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Cache everything` (`cache: true`)
* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno) o `Respect origin`
* **Browser TTL**: `Respect origin`
* **Cache Key**:
  * Query String: `Ignore query string` (oppure escludere parametri marketing: `fbclid`, `gclid`, `utm_*`)

---

### Condizioni con Commenti

#### 1. Metodi di Richiesta Idonei alla Cache
Abilita la memorizzazione in cache per tutte le richieste GET e HEAD pubbliche non intercettate dalla regola di bypass precedente.
```text
http.request.method in {"GET" "HEAD"}
```

---

### Espressione Standalone (Se non si usa la regola di Bypass separata)

```text
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout" or http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/section/load" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql" or http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version"))
```

### Espressione Accoppiata (Se prima è già attiva la Cache Whitelist di Bypass)

```text
http.request.method in {"GET" "HEAD"}
```
