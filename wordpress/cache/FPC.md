# FULL PAGE CACHE (FPC) - WORDPRESS

Questa regola definisce **COSA CACHARE** a livello di Edge Cloudflare per WordPress (articoli, pagine, categorie, homepage).

### Azione Cloudflare (Cache Rule)
* **Eligible for cache**: `Cache everything` (`cache: true`)
* **Edge TTL**: `Override origin` -> `86400 seconds` (1 giorno)
* **Browser TTL**: `Respect origin`

---

### Condizioni con Commenti

#### 1. Metodi di richiesta supportati per la cache
Consente la memorizzazione in cache solo per le richieste di lettura idempotenti (GET e HEAD).
```text
http.request.method in {"GET" "HEAD"}
```

#### 2. Solo traffico pubblico (quando usata come regola stand-alone con esclusione integrata)
Esclude il pannello di controllo, le API e le sessioni di utenti loggati.
```text
not (http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.cookie contains "wordpress_logged_in_" or http.cookie contains "comment_author_")
```

---

### Espressione Standalone

```text
(http.request.method in {"GET" "HEAD"} and not (http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login" or http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php" or http.cookie contains "wordpress_logged_in_" or http.cookie contains "comment_author_"))
```

### Espressione Accoppiata (Se prima è già attiva la Cache Whitelist di Bypass)

```text
http.request.method in {"GET" "HEAD"}
```
