# FULL PAGE CACHE (FPC) - WOOCOMMERCE

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare per velocizzare al massimo la navigazione pubblica (pagine catalogo, prodotti, categorie, homepage).

### Posizione nella Ruleset
Deve trovarsi **dopo** la regola di Cache Whitelist / Bypass.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Cache everything` (`cache: true`)
* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno) oppure impostabile a seconda delle esigenze
* **Browser TTL**: `Respect origin`
* **Cache Key**:
  * Query String: `Ignore query string` (oppure personalizzata escludendo parametri di tracking marketing come `fbclid`, `gclid`, `utm_*`)

---

### Condizioni con Commenti

#### 1. Metodi di richiesta supportati per la cache
Consente la memorizzazione in cache solo per le richieste di lettura idempotenti (GET e HEAD).
```text
http.request.method in {"GET" "HEAD"}
```

#### 2. Solo traffico pubblico (quando usata come regola stand-alone con esclusione integrata)
Esclude tutte le pagine private, carrelli, sessioni utente e percorsi amministrativi per cachare solo la navigazione del catalogo pubblico.
```text
not (http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/addons" or http.request.uri.query contains "add-to-cart" or http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "wp_woocommerce_session_" or http.cookie contains "wordpress_logged_in_")
```

---

### Espressione Standalone (Se non si usa la regola di Bypass separata)

```text
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/addons" or http.request.uri.query contains "add-to-cart" or http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "wp_woocommerce_session_" or http.cookie contains "wordpress_logged_in_"))
```

### Espressione Accoppiata (Se prima è già attiva la Cache Whitelist di Bypass)

```text
http.request.method in {"GET" "HEAD"}
```
