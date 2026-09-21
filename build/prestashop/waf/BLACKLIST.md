# BLACKLIST - PRESTASHOP

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Blocco (Block 403)` (`action: block`)

### Descrizione
Blocco immediato (403) per richieste alla ricerca e filtri PrestaShop (controller=search o ?s=) prive di referer interno valido.

---

### Condizioni Dettagliate con Commenti

#### Ricerca PrestaShop senza Referer Interno
Blocca chiamate dirette alla ricerca PrestaShop prive di referer del sito.
```text
(http.request.uri.query contains "controller=search" or http.request.uri.query contains "s=" or http.request.uri.path contains "/cerca") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(http.request.uri.query contains "controller=search" or http.request.uri.query contains "s=" or http.request.uri.path contains "/cerca") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```
