# CACHE WHITELIST (BYPASS CACHE) - WORDPRESS

Questa regola identifica tutte le richieste dinamiche, login, commenti e admin che **NON devono essere cachate** da Cloudflare.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

#### 1. Amministrazione WordPress & Login
Pannello di controllo WordPress e pagina di login amministrativo che richiedono sempre elaborazione dinamica.
```text
http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login"
```

#### 2. Endpoint REST API & XML-RPC
Chiamate REST API e interfacce XML-RPC che richiedono risposte sempre aggiornate.
```text
http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php"
```

#### 3. Cookie Utente Autenticato WordPress
Cookie generato all'autenticazione dell'utente per mostrare la barra di amministrazione e contenuti riservati.
```text
http.cookie contains "wordpress_logged_in_"
```

#### 4. Cookie Autore Commenti
Cookie memorizzato quando un visitatore lascia un commento per compilare automaticamente i campi.
```text
http.cookie contains "comment_author_"
```

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.cookie contains "wordpress_logged_in_" or http.cookie contains "comment_author_")
```
