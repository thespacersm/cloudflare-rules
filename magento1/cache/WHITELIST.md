# CACHE WHITELIST (BYPASS CACHE) - MAGENTO 1

Questa regola definisce tutte le richieste dinamiche, carrelli, sessioni cliente, cassa e backend di **Magento 1** che **NON devono essere cachate** da Cloudflare.

### Posizione nella Ruleset
Deve trovarsi **prima** della regola di FPC (priorità più alta).

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

#### 1. Carrello e Cassa (Standard e OneStepCheckout)
Pagine di visualizzazione carrello e flussi di checkout standard o basati su estensioni (es. OneStepCheckout / Idev).
```text
http.request.uri.path contains "/checkout/cart" or http.request.uri.path contains "/checkout/onepage" or http.request.uri.path contains "/onestepcheckout"
```

#### 2. Area Cliente e Autenticazione
Pagine di login, registrazione e dashboard personale del cliente (storico ordini, indirizzi, wishlist).
```text
http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login"
```

#### 3. Pannello Amministrativo (Adminhtml)
Area di backend Magento per la gestione del negozio e degli ordini.
```text
http.request.uri.path contains "/admin" or http.request.uri.path contains "/index.php/admin"
```

#### 4. API SOAP, XML-RPC e REST
Endpoint nativi di Magento per integrazioni gestionali, ERP e connettori esterni.
```text
http.request.uri.path contains "/api/" or http.request.uri.path contains "/api/soap" or http.request.uri.path contains "/api/rest" or http.request.uri.path contains "/oauth"
```

#### 5. Cookie di Sessione Frontend e Carrello
Il cookie `frontend` identifica univocamente la sessione del visitatore in Magento 1 non appena interagisce con il carrello o effettua il login.
```text
http.cookie contains "frontend"
```

#### 6. Cookie di Sessione Amministratore
Cookie generato all'accesso dell'amministratore nel pannello di controllo.
```text
http.cookie contains "adminhtml"
```

---

### Tabella di Riepilogo

| Ambito | Tipo | Condizione | Motivazione |
| :--- | :--- | :--- | :--- |
| **Carrello & Checkout** | Path | `http.request.uri.path contains "/checkout/" or "/onestepcheckout"` | Flusso transazionale e acquisto |
| **Area Riservata** | Path | `http.request.uri.path contains "/customer/account"` | Dati personali e ordini del cliente |
| **Backend Admin** | Path | `http.request.uri.path contains "/admin"` | Gestione catalogo e ordini |
| **Integrazioni API** | Path | `http.request.uri.path contains "/api/" or "/oauth"` | Comunicazione con gestionali esterni |
| **Sessione Utente** | Cookie | `http.cookie contains "frontend"` | Sessione attiva o articoli nel carrello |
| **Sessione Admin** | Cookie | `http.cookie contains "adminhtml"` | Accesso operatore di backend |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/checkout/cart" or http.request.uri.path contains "/checkout/onepage" or http.request.uri.path contains "/onestepcheckout" or http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/admin" or http.request.uri.path contains "/api/" or http.request.uri.path contains "/oauth" or http.cookie contains "frontend" or http.cookie contains "adminhtml")
```
