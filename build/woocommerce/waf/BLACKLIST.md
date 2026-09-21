# BLACKLIST - WOOCOMMERCE

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Blocco (Block 403)` (`action: block`)

### Descrizione
Blocco immediato (403) per qualsiasi richiesta verso la ricerca interna (?s= o /search/) o con filtri prodotto (filter_*, min_price, max_price) priva di referer interno valido.

---

### Condizioni Dettagliate con Commenti

#### Ricerca e Filtri WooCommerce senza Referer Interno
Blocca richieste alla ricerca e ai filtri layered navigation di WooCommerce se prive di referer interno.
```text
(http.request.uri.query contains "s=" or http.request.uri.path contains "/search/" or http.request.uri.query contains "filter_" or http.request.uri.query contains "min_price" or http.request.uri.query contains "max_price") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(http.request.uri.query contains "s=" or http.request.uri.path contains "/search/" or http.request.uri.query contains "filter_" or http.request.uri.query contains "min_price" or http.request.uri.query contains "max_price") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```
