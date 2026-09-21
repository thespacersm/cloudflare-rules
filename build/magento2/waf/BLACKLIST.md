# BLACKLIST - MAGENTO 2

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Blocco (Block 403)` (`action: block`)

### Descrizione
Blocco immediato (403) per qualsiasi richiesta verso la ricerca interna (catalogsearch) o con filtri layered navigation (%2c o ,) priva di referer interno valido.

---

### Condizioni Dettagliate con Commenti

#### Ricerca e Filtri senza Referer Interno
Blocca bot e script che eseguono query di ricerca gravose su Magento 2 (catalogsearch) o combinazioni di filtri layered navigation senza passare dalla normale navigazione del sito.
```text
(http.request.uri.path contains "catalogsearch" or lower(http.request.uri.query) contains "%2c" or http.request.uri.query contains ",") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(http.request.uri.path contains "catalogsearch" or lower(http.request.uri.query) contains "%2c" or http.request.uri.query contains ",") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```
