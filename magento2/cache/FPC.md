# FULL PAGE CACHE (FPC) - MAGENTO 2

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare. Nella logica a due regole, questa regola memorizza in cache **tutto il traffico pubblico**, poiché tutte le pagine dinamiche, carrelli e sessioni sono già state intercettate e skippate dalla regola **Cache Whitelist (Bypass)**.

### Ordine di Esecuzione delle Regole (Cloudflare Cache Rules)
Nel Ruleset Engine di Cloudflare per le Cache Rules, **l'ultima regola che matcha ha la precedenza** (sovrascrive le impostazioni delle precedenti).

Pertanto, l'ordine di inserimento è:
1. **Regola 1 (FPC - Cache Everything)**: abilita la cache su tutte le richieste pubbliche `http.request.method in {"GET" "HEAD"}`.
2. **Regola 2 (Whitelist - Bypass Cache)**: posizionata **sotto/dopo** l'FPC, intercetta le eccezioni del CMS (carrello, admin, login, cookie) e imposta `Bypass cache` (`cache: false`), sovrascrivendo l'FPC.

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
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout" or http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login" or http.request.uri.path contains "/customer/section/load" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql" or http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version"))
```
