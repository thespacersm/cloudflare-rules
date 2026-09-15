# CACHE WHITELIST (BYPASS CACHE) - WORDPRESS

Bypassa la cache per pannello di controllo WordPress, login, API e sessioni utente loggato.

### Posizione nella Ruleset
Nel motore Cache Rules di Cloudflare l'ultima regola che matcha sovrascrive le precedenti.
Questa regola di bypass deve essere posizionata **dopo / sotto** la regola di FPC, in modo da avere priorità di override.

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

### Tabella di Riepilogo

| Ambito | Condizione | Motivazione |
| :--- | :--- | :--- |
| **Amministrazione WordPress & Login** | `http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login"` | Pannello di controllo WordPress e pagina di login amministrativo che richiedono sempre elaborazione dinamica. |
| **Endpoint REST API & XML-RPC** | `http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php"` | Chiamate REST API e interfacce XML-RPC che richiedono risposte sempre aggiornate. |
| **Cookie Utente Autenticato WordPress** | `http.cookie contains "wordpress_logged_in_"` | Cookie generato all'autenticazione dell'utente per mostrare la barra di amministrazione e contenuti riservati. |
| **Cookie Autore Commenti** | `http.cookie contains "comment_author_"` | Cookie memorizzato quando un visitatore lascia un commento per compilare automaticamente i campi. |

---

### Espressione Completa (Bypass Cache)

```text
(http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login") or (http.request.uri.path contains "/wp-json" or http.request.uri.path contains "/xmlrpc.php") or (http.cookie contains "wordpress_logged_in_") or (http.cookie contains "comment_author_")
```
