# FULL PAGE CACHE (FPC) - WORDPRESS

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare per WordPress (articoli, pagine, categorie, homepage).

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Cache everything` (`cache: true`)
* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno)
* **Browser TTL**: `Respect origin`

---

### Espressione Standalone

```text
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.cookie contains "wordpress_logged_in_" or http.cookie contains "comment_author_"))
```

### Espressione Accoppiata (Se prima è già attiva la Cache Whitelist di Bypass)

```text
http.request.method in {"GET" "HEAD"}
```
