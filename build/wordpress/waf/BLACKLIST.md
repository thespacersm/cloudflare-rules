# BLACKLIST - WORDPRESS

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Verifica interattiva (Managed Challenge)` (`action: managed_challenge`)

### Descrizione
Richiede una Verifica Interattiva (Cloudflare Turnstile) per tutti i visitatori con geolocalizzazione IP esterna ad Italia (IT), San Marino (SM) e Città del Vaticano (VA), oppure per richieste alla ricerca interna prive di referer.

---

### Condizioni Dettagliate con Commenti

#### Blocco Nazioni Estere
Sfida con verifica interattiva tutti i visitatori provenienti da paesi diversi da Italia, San Marino e Città del Vaticano.
```text
not ip.src.country in {"IT" "SM" "VA"}
```

#### Ricerca senza Referer
Sfida con verifica interattiva chiunque invochi la ricerca interna WordPress senza referer.
```text
(http.request.uri.query contains "s=" or http.request.uri.path contains "/search/") and (http.referer eq "" or not http.referer contains "{DOMAIN}")
```

---

### Espressione Completa (Cloudflare Expression Builder)

> [!NOTE]
> Sostituisci `{DOMAIN}` con il dominio effettivo del sito (es. `mysite.com`).

```text
(not ip.src.country in {"IT" "SM" "VA"}) or ((http.request.uri.query contains "s=" or http.request.uri.path contains "/search/") and (http.referer eq "" or not http.referer contains "{DOMAIN}"))
```
