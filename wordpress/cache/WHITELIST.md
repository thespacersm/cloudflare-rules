# CACHE WHITELIST (BYPASS CACHE) - WORDPRESS

Questa regola identifica tutte le richieste dinamiche, login, commenti e admin che **NON devono essere cachate** da Cloudflare.

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Bypass cache` (`cache: false`)

---

### Condizioni Dettagliate con Commenti

# 1. Amministrazione WordPress & Login
http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login"

# 2. Endpoint REST API & XML-RPC
http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php"

# 3. Cookie Utente Autenticato WordPress
http.cookie contains "wordpress_logged_in_"

# 4. Cookie Autore Commenti
http.cookie contains "comment_author_"

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.cookie contains "wordpress_logged_in_" or http.cookie contains "comment_author_")
```
