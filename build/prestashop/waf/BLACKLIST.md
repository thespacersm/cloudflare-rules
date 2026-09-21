# BLACKLIST - PRESTASHOP

### Azione Cloudflare (WAF Custom Rule)
* **Azione**: `Verifica interattiva (Managed Challenge)` (`action: managed_challenge`)

### Descrizione
Richiede una Verifica Interattiva (Cloudflare Turnstile) per tutti i visitatori con geolocalizzazione IP esterna ad Italia (IT), San Marino (SM) e Città del Vaticano (VA).

---

### Condizioni Dettagliate con Commenti

#### Blocco Nazioni Estere
Sfida con verifica interattiva tutti i visitatori provenienti da paesi diversi da Italia, San Marino e Città del Vaticano.
```text
not ip.src.country in {"IT" "SM" "VA"}
```

---

### Espressione Completa (Cloudflare Expression Builder)

```text
(not ip.src.country in {"IT" "SM" "VA"})
```
