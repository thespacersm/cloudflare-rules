# CACHE WHITELIST (BYPASS CACHE) - MAGENTO 1

Bypassa la cache per checkout, carrello, area cliente, adminhtml e sessione frontend di Magento 1.

### Posizione nella Ruleset
Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.
Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.

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
Il cookie frontend identifica univocamente la sessione del visitatore in Magento 1 non appena interagisce con il carrello o effettua il login.
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

| Ambito | Condizione | Motivazione |
| :--- | :--- | :--- |
| **Carrello e Cassa (Standard e OneStepCheckout)** | `http.request.uri.path contains "/checkout/cart" or http.request.uri.path contains "/checkout/onepage" or http.request.uri.path contains "/onestepcheckout"` | Pagine di visualizzazione carrello e flussi di checkout standard o basati su estensioni (es. OneStepCheckout / Idev). |
| **Area Cliente e Autenticazione** | `http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login"` | Pagine di login, registrazione e dashboard personale del cliente (storico ordini, indirizzi, wishlist). |
| **Pannello Amministrativo (Adminhtml)** | `http.request.uri.path contains "/admin" or http.request.uri.path contains "/index.php/admin"` | Area di backend Magento per la gestione del negozio e degli ordini. |
| **API SOAP, XML-RPC e REST** | `http.request.uri.path contains "/api/" or http.request.uri.path contains "/api/soap" or http.request.uri.path contains "/api/rest" or http.request.uri.path contains "/oauth"` | Endpoint nativi di Magento per integrazioni gestionali, ERP e connettori esterni. |
| **Cookie di Sessione Frontend e Carrello** | `http.cookie contains "frontend"` | Il cookie frontend identifica univocamente la sessione del visitatore in Magento 1 non appena interagisce con il carrello o effettua il login. |
| **Cookie di Sessione Amministratore** | `http.cookie contains "adminhtml"` | Cookie generato all'accesso dell'amministratore nel pannello di controllo. |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/checkout/cart" or http.request.uri.path contains "/checkout/onepage" or http.request.uri.path contains "/onestepcheckout") or (http.request.uri.path contains "/customer/account" or http.request.uri.path contains "/customer/account/login") or (http.request.uri.path contains "/admin" or http.request.uri.path contains "/index.php/admin") or (http.request.uri.path contains "/api/" or http.request.uri.path contains "/api/soap" or http.request.uri.path contains "/api/rest" or http.request.uri.path contains "/oauth") or (http.cookie contains "frontend") or (http.cookie contains "adminhtml")
```
