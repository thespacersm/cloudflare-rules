# CACHE WHITELIST (BYPASS CACHE) - MAGENTO 2

Questa regola definisce tutte le richieste dinamiche, carrelli, sezioni private AJAX, cassa e backend di **Magento 2** che **NON devono essere cachate** da Cloudflare.

### Posizione nella Ruleset
Deve trovarsi **prima** della regola di FPC (priorità più alta).

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
Endpoint fondamentale di Magento 2: `customer/section/load` carica via AJAX i blocchi privati (minicart, nome utente) sopra le pagine pubbliche cachate. Non deve MAI essere cachato.
```text
http.request.uri.path contains "/customer/section/load"
```

#### 4. Pannello di Controllo Amministrativo
Area di amministrazione backend (può trovarsi su `/admin` o su URL personalizzato generato all'installazione).
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

| Ambito | Tipo | Condizione | Motivazione |
| :--- | :--- | :--- | :--- |
| **Carrello & Checkout** | Path | `http.request.uri.path contains "/checkout"` | Gestione acquisti in corso |
| **Sezioni Private AJAX** | Path | `http.request.uri.path contains "/customer/section/load"` | Minicart e blocchi utente dinamici |
| **Area Riservata** | Path | `http.request.uri.path contains "/customer/account"` | Profilo, indirizzi e ordini |
| **Backend Admin** | Path | `http.request.uri.path contains "/admin"` | Accesso amministrazione del sito |
| **API & Headless** | Path | `http.request.uri.path contains "/rest/" or "/graphql"` | Chiamate dati in tempo reale |
| **Sessione Attiva** | Cookie | `http.cookie contains "PHPSESSID" or "private_content_version"` | Riconoscimento carrello o utente connesso |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/checkout" or http.request.uri.path contains "/onestepcheckout" or http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/section/load" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/rest/" or http.request.uri.path contains "/graphql" or http.cookie contains "PHPSESSID" or http.cookie contains "private_content_version")
```
