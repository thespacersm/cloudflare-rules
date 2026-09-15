# CACHE WHITELIST (BYPASS CACHE) - PRESTASHOP

Bypassa la cache per carrello, ordine, account cliente, back office e sessioni PrestaShop.

### Posizione nella Ruleset
Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.
Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

#### 1. Carrello e Checkout (Multilingua)
Pagine di visualizzazione carrello, step di ordinazione e conferma acquisto nelle diverse lingue supportate (IT, EN, FR, ES).
```text
http.request.uri.path contains "/cart" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/panier" or http.request.uri.path contains "/order" or http.request.uri.path contains "/ordine" or http.request.uri.path contains "/commande" or http.request.uri.path contains "/order-confirmation"
```

#### 2. Area Cliente e Login
Pagine di autenticazione, recupero password e pannello dell'account cliente.
```text
http.request.uri.path contains "/my-account" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "/mon-compte" or http.request.uri.path contains "/login" or http.request.uri.path contains "/autenticazione" or http.request.uri.path contains "/authentication"
```

#### 3. Back Office Amministrazione
Pannello di controllo PrestaShop (normalmente collocato in una sottocartella /admin o con suffisso casuale es. /admin1234/).
```text
http.request.uri.path contains "/admin"
```

#### 4. WebService API e Moduli di Pagamento
API REST native di PrestaShop e chiamate AJAX/webhook gestite dai moduli (es. pagamenti o corrieri).
```text
http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/"
```

#### 5. Cookie di Sessione PrestaShop
Cookie univoco di sessione generato da PrestaShop (inizia sempre per PrestaShop- seguito dall'hash dell'installazione) che mantiene il carrello e lo stato dell'utente.
```text
http.cookie contains "PrestaShop-"
```

---

### Tabella di Riepilogo

| Ambito | Condizione | Motivazione |
| :--- | :--- | :--- |
| **Carrello e Checkout (Multilingua)** | `http.request.uri.path contains "/cart" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/panier" or http.request.uri.path contains "/order" or http.request.uri.path contains "/ordine" or http.request.uri.path contains "/commande" or http.request.uri.path contains "/order-confirmation"` | Pagine di visualizzazione carrello, step di ordinazione e conferma acquisto nelle diverse lingue supportate (IT, EN, FR, ES). |
| **Area Cliente e Login** | `http.request.uri.path contains "/my-account" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "/mon-compte" or http.request.uri.path contains "/login" or http.request.uri.path contains "/autenticazione" or http.request.uri.path contains "/authentication"` | Pagine di autenticazione, recupero password e pannello dell'account cliente. |
| **Back Office Amministrazione** | `http.request.uri.path contains "/admin"` | Pannello di controllo PrestaShop (normalmente collocato in una sottocartella /admin o con suffisso casuale es. /admin1234/). |
| **WebService API e Moduli di Pagamento** | `http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/"` | API REST native di PrestaShop e chiamate AJAX/webhook gestite dai moduli (es. pagamenti o corrieri). |
| **Cookie di Sessione PrestaShop** | `http.cookie contains "PrestaShop-"` | Cookie univoco di sessione generato da PrestaShop (inizia sempre per PrestaShop- seguito dall'hash dell'installazione) che mantiene il carrello e lo stato dell'utente. |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/cart" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/panier" or http.request.uri.path contains "/order" or http.request.uri.path contains "/ordine" or http.request.uri.path contains "/commande" or http.request.uri.path contains "/order-confirmation") or (http.request.uri.path contains "/my-account" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "/mon-compte" or http.request.uri.path contains "/login" or http.request.uri.path contains "/autenticazione" or http.request.uri.path contains "/authentication") or (http.request.uri.path contains "/admin") or (http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/") or (http.cookie contains "PrestaShop-")
```
