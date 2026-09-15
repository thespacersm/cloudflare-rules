# FULL PAGE CACHE (FPC) - WOOCOMMERCE

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare. Nella logica a due regole, questa regola memorizza in cache **tutto il traffico pubblico** (pagine catalogo, schede prodotto, categorie, homepage, blog), poiché tutte le pagine dinamiche, carrelli e sessioni sono già state intercettate e skippate dalla regola precedente **Cache Whitelist (Bypass)**.

### Ordine di Esecuzione delle Regole (Cloudflare Cache Rules)
Nel Ruleset Engine di Cloudflare per le Cache Rules, **l'ultima regola che matcha ha la precedenza** (sovrascrive le impostazioni delle precedenti).

Pertanto, l'ordine di inserimento è:
1. **Regola 1 (FPC - Cache Everything)**: abilita la cache su tutte le richieste pubbliche `http.request.method in {"GET" "HEAD"}`.
2. **Regola 2 (Whitelist - Bypass Cache)**: posizionata **sotto/dopo** l'FPC, intercetta le eccezioni del CMS (carrello, admin, login, cookie) e imposta `Bypass cache` (`cache: false`), sovrascrivendo l'FPC.

1. **Regola 1 (Priorità 1 - Bypass)**: definita in [`WHITELIST.md`](./WHITELIST.md), esclude carrello, checkout, account utente, admin, API e cookie di sessione.
2. **Regola 2 (Priorità 2 - FPC Tutto)**: questa regola, memorizza in cache tutto il traffico di navigazione rimanente.

---

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Cache everything` (`cache: true`)
* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno) o personalizzato
* **Browser TTL**: `Respect origin`
* **Cache Key**:
  * Query String: `Ignore query string` (oppure personalizzata escludendo parametri di tracking come `fbclid`, `gclid`, `utm_*`)

---

### Espressione Principale (Modello a 2 Regole)

Poiché le eccezioni dinamiche sono gestite a monte da `WHITELIST.md`, l'espressione per cachare tutto il traffico pubblico è semplicemente:

#### 1. Metodi HTTP Idonei alla Cache
Memorizza in cache qualsiasi richiesta di lettura GET o HEAD per la navigazione pubblica.
```text
http.request.method in {"GET" "HEAD"}
```

---

### Variante Standalone (Regola Singola con Esclusioni Integrate)

Se preferisci creare una sola regola anziché due separate, puoi inserire le esclusioni direttamente nell'FPC:

```text
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/addons" or http.request.uri.query contains "add-to-cart" or http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "wp_woocommerce_session_" or http.cookie contains "wordpress_logged_in_"))
```
