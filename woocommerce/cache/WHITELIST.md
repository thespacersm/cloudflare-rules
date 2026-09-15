# CACHE WHITELIST (BYPASS CACHE) - WOOCOMMERCE

Bypassa la cache per carrello, cassa, account cliente, API WooCommerce e cookie di sessione carrello.

### Posizione nella Ruleset
Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.
Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

#### 1. Carrello, Cassa e Account Utente (IT & EN)
Pagine dinamiche e personalizzate per ogni cliente contenenti carrello, checkout e dashboard account, sia in lingua italiana che inglese.
```text
http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account"
```

#### 2. Amministrazione WordPress & Login
Pannello di controllo WordPress e pagina di login amministrativo che richiedono sempre elaborazione dinamica.
```text
http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login"
```

#### 3. Endpoint API, Webhook e XML-RPC
Chiamate REST API, webhook di pagamento, interfacce XML-RPC e addon WooCommerce che devono scambiare dati in tempo reale.
```text
http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/addons"
```

#### 4. Query String di Carrello
Parametri GET utilizzati da WooCommerce per l'aggiunta diretta di prodotti al carrello via URL.
```text
http.request.uri.query contains "add-to-cart"
```

#### 5. Cookie di Sessione Carrello WooCommerce
Cookie rilasciati da WooCommerce non appena un utente aggiunge un prodotto al carrello, necessari per non mostrare pagine cachate con carrello vuoto.
```text
http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "woocommerce_cart_hash" or http.cookie contains "wp_woocommerce_session_"
```

#### 6. Cookie Utente Loggato WordPress
Cookie generato all'autenticazione dell'utente (cliente o amministratore) per mostrare barre personalizzate e contenuti riservati.
```text
http.cookie contains "wordpress_logged_in_"
```

---

### Tabella di Riepilogo

| Ambito | Condizione | Motivazione |
| :--- | :--- | :--- |
| **Carrello, Cassa e Account Utente (IT & EN)** | `http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account"` | Pagine dinamiche e personalizzate per ogni cliente contenenti carrello, checkout e dashboard account, sia in lingua italiana che inglese. |
| **Amministrazione WordPress & Login** | `http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login"` | Pannello di controllo WordPress e pagina di login amministrativo che richiedono sempre elaborazione dinamica. |
| **Endpoint API, Webhook e XML-RPC** | `http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/addons"` | Chiamate REST API, webhook di pagamento, interfacce XML-RPC e addon WooCommerce che devono scambiare dati in tempo reale. |
| **Query String di Carrello** | `http.request.uri.query contains "add-to-cart"` | Parametri GET utilizzati da WooCommerce per l'aggiunta diretta di prodotti al carrello via URL. |
| **Cookie di Sessione Carrello WooCommerce** | `http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "woocommerce_cart_hash" or http.cookie contains "wp_woocommerce_session_"` | Cookie rilasciati da WooCommerce non appena un utente aggiunge un prodotto al carrello, necessari per non mostrare pagine cachate con carrello vuoto. |
| **Cookie Utente Loggato WordPress** | `http.cookie contains "wordpress_logged_in_"` | Cookie generato all'autenticazione dell'utente (cliente o amministratore) per mostrare barre personalizzate e contenuti riservati. |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/cart" or http.request.uri.path contains "/checkout" or http.request.uri.path contains "/my-account" or http.request.uri.path contains "/carrello" or http.request.uri.path contains "/cassa" or http.request.uri.path contains "/mio-account") or (http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login") or (http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/wc-api" or http.request.uri.path contains "/xmlrpc.php" or http.request.uri.path contains "/addons") or (http.request.uri.query contains "add-to-cart") or (http.cookie contains "woocommerce_items_in_cart" or http.cookie contains "woocommerce_cart_hash" or http.cookie contains "wp_woocommerce_session_") or (http.cookie contains "wordpress_logged_in_")
```
