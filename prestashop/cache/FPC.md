# FULL PAGE CACHE (FPC) - PRESTASHOP

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare. Nella logica a due regole, questa regola memorizza in cache **tutto il traffico pubblico** (home, categorie, schede prodotto, produttori, pagine CMS), poiché tutte le pagine dinamiche, carrelli e sessioni sono già state intercettate e skippate dalla regola precedente **Cache Whitelist (Bypass)**.

### Architettura a 2 Regole (Cloudflare Cache Rules)
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
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/cart" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/panier" or http.request.uri.path contains "/order" or http.request.uri.path contains "/ordine" or http.request.uri.path contains "/commande" or http.request.uri.path contains "/order-confirmation" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "/mon-compte" or http.request.uri.path contains "/login" or http.request.uri.path contains "/autenticazione" or http.request.uri.path contains "/authentication" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/" or http.cookie contains "PrestaShop-"))
```
