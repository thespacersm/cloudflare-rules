# BLACKLIST - WOOCOMMERCE

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Verifica interattiva (Managed Challenge)` (`action: managed_challenge`)

### Descrizione
Richiede una Verifica Interattiva (Cloudflare Turnstile) per tutti i visitatori con geolocalizzazione IP esterna ad Italia (IT), San Marino (SM) e Città del Vaticano (VA), oppure per qualsiasi richiesta verso la ricerca interna (?s= o /search/) o con filtri prodotto (filter_*, min_price, max_price) priva di referer interno valido.

---

### Condizioni Dettagliate con Commenti

#### Blocco Nazioni Estere
Sfida con verifica interattiva tutti i visitatori provenienti da paesi diversi da Italia, San Marino e Città del Vaticano.
```text
not ip.src.country in {"IT" "SM" "VA"}
```

#### Ricerca e Filtri senza Referer Interno
Blocca/sfida chiamate automatiche alla ricerca WordPress/WooCommerce (?s= o /search/) o a parametri di filtraggio prodotto senza referer valido.
```text
(http.request.uri.query contains "s=" or http.request.uri.path contains "/search/" or http.request.uri.query contains "filter_" or http.request.uri.query contains "min_price" or http.request.uri.query contains "max_price") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(not ip.src.country in {"IT" "SM" "VA"}) or ((http.request.uri.query contains "s=" or http.request.uri.path contains "/search/" or http.request.uri.query contains "filter_" or http.request.uri.query contains "min_price" or http.request.uri.query contains "max_price") and (http.referer eq "" or not http.referer contains "{DOMAIN}"))
```
