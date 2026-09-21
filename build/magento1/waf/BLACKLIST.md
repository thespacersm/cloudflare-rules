# BLACKLIST - MAGENTO 1

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Verifica interattiva (Interactive Challenge)` (`action: interactive_challenge`)

### Descrizione
Richiede una Verifica Interattiva (Cloudflare Turnstile) per tutti i visitatori con geolocalizzazione IP esterna ad Italia (IT), San Marino (SM) e Città del Vaticano (VA), oppure per qualsiasi richiesta verso la ricerca interna (catalogsearch) o con filtri layered navigation (%2c o ,) priva di referer interno valido.

---

### Condizioni Dettagliate con Commenti

#### Blocco Nazioni Estere
Sfida con verifica interattiva tutti i visitatori provenienti da paesi diversi da Italia, San Marino e Città del Vaticano.
```text
not ip.src.country in {"IT" "SM" "VA"}
```

#### Ricerca e Filtri senza Referer Interno
Intercetta bot e scanner che eseguono query di ricerca gravose su Magento 1 (catalogsearch) o combinazioni di filtri layered navigation senza passare dalla navigazione del sito.
```text
(http.request.uri.path contains "catalogsearch" or lower(http.request.uri.query) contains "%2c" or http.request.uri.query contains ",") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(not ip.src.country in {"IT" "SM" "VA"}) or ((http.request.uri.path contains "catalogsearch" or lower(http.request.uri.query) contains "%2c" or http.request.uri.query contains ",") and (http.referer eq "" or not http.referer contains "{DOMAIN}"))
```
