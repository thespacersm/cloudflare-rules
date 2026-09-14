# CACHE WHITELIST (BYPASS CACHE) - PRESTASHOP

Questa regola definisce tutte le richieste dinamiche, carrelli, cassa, account cliente e pannello di **PrestaShop** che **NON devono essere cachate** da Cloudflare.

### Posizione nella Ruleset
Deve trovarsi **prima** della regola di FPC (priorità più alta).

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
Pannello di controllo PrestaShop (normalmente collocato in una sottocartella `/admin` o con suffisso casuale es. `/admin1234/`).
```text
http.request.uri.path contains "/admin"
```

#### 4. WebService API e Moduli di Pagamento
API REST native di PrestaShop e chiamate AJAX/webhook gestite dai moduli (es. pagamenti o corrieri).
```text
http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/"
```

#### 5. Cookie di Sessione PrestaShop
Cookie univoco di sessione generato da PrestaShop (inizia sempre per `PrestaShop-` seguito dall'hash dell'installazione) che mantiene il carrello e lo stato dell'utente.
```text
http.cookie contains "PrestaShop-"
```

---

### Tabella di Riepilogo

| Ambito | Tipo | Condizione | Motivazione |
| :--- | :--- | :--- | :--- |
| **Carrello & Ordine** | Path | `http.request.uri.path in {"/carrello" "/ordine" "/cart" ...}` | Processo d'acquisto dinamico |
| **Area Riservata** | Path | `http.request.uri.path in {"/mio-account" "/autenticazione" ...}` | Accesso e dati personali |
| **Back Office** | Path | `http.request.uri.path contains "/admin"` | Gestione del negozio |
| **API & Moduli** | Path | `http.request.uri.path contains "/api/" or "/module/"` | Webhook di pagamento e connettori |
| **Sessione Attiva** | Cookie | `http.cookie contains "PrestaShop-"` | Riconoscimento carrello o utente connesso |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/cart" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/panier" or http.request.uri.path contains "/order" or http.request.uri.path contains "/ordine" or http.request.uri.path contains "/commande" or http.request.uri.path contains "/order-confirmation" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/mio-account" or http.request.uri.path contains "/mon-compte" or http.request.uri.path contains "/login" or http.request.uri.path contains "/autenticazione" or http.request.uri.path contains "/authentication" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/api/" or http.request.uri.path contains "/module/" or http.cookie contains "PrestaShop-")
```
