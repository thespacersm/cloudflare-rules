# CACHE WHITELIST (BYPASS CACHE) - MAGENTO 2

Bypassa la cache per checkout, sezioni private AJAX, area cliente, admin, API e sessioni di Magento 2.

### Posizione nella Ruleset
Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.
Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

#### 1. Carrello, Cassa e Flussi Checkout
Pagine dinamiche del carrello e del flusso di checkout standard o one-step.
```text
http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout"
```

#### 2. Area Cliente e Dati Personali
Pagine di autenticazione e gestione account cliente.
```text
http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login"
```

#### 3. Chiamate AJAX a Sezioni Private (Carrello Dinamico / User Info)
Endpoint fondamentale di Magento 2: customer/section/load carica via AJAX i blocchi privati (minicart, nome utente) sopra le pagine pubbliche cachate. Non deve MAI essere cachato.
```text
http.request.uri.path contains "/customer/section/load"
```

#### 4. Pannello di Controllo Amministrativo
Area di amministrazione backend (può trovarsi su /admin o su URL personalizzato generato all'installazione).
```text
http.request.uri.path contains "/admin"
```

#### 5. Endpoint REST API e GraphQL
Chiamate per frontend headless, app mobile, sync magazzino ed ERP.
```text
http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql"
```

#### 6. Cookie di Sessione e Stato Privato Magento 2
Cookie generati per identificare sessioni PHP attive, chiavi CSRF del form o versioni del contenuto privato.
```text
http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version"
```

---

### Tabella di Riepilogo

| Ambito | Condizione | Motivazione |
| :--- | :--- | :--- |
| **Carrello, Cassa e Flussi Checkout** | `http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout"` | Pagine dinamiche del carrello e del flusso di checkout standard o one-step. |
| **Area Cliente e Dati Personali** | `http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login"` | Pagine di autenticazione e gestione account cliente. |
| **Chiamate AJAX a Sezioni Private (Carrello Dinamico / User Info)** | `http.request.uri.path contains "/customer/section/load"` | Endpoint fondamentale di Magento 2: customer/section/load carica via AJAX i blocchi privati (minicart, nome utente) sopra le pagine pubbliche cachate. Non deve MAI essere cachato. |
| **Pannello di Controllo Amministrativo** | `http.request.uri.path contains "/admin"` | Area di amministrazione backend (può trovarsi su /admin o su URL personalizzato generato all'installazione). |
| **Endpoint REST API e GraphQL** | `http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql"` | Chiamate per frontend headless, app mobile, sync magazzino ed ERP. |
| **Cookie di Sessione e Stato Privato Magento 2** | `http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version"` | Cookie generati per identificare sessioni PHP attive, chiavi CSRF del form o versioni del contenuto privato. |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout") or (http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login") or (http.request.uri.path contains "/customer/section/load") or (http.request.uri.path contains "/admin") or (http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql") or (http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version")
```
