# WAF WHITELIST - MAGENTO2

### Azione
`Skip`
- Skip all remaining rules in current ruleset
- Phase: `http_ratelimit`, `http_request_firewall_managed`, `http_request_sbfm`
- Products: `WAF`, `Rate Limiting`, `Security Level`, `Zone Lockdown`, `User Agent Blocking`, `Browser Integrity Check`

---

### Regole e Condizioni con Commenti

**DOOFINDER CRAWLER (IP EU, USA, ASIA)**
ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}

**PAGAMENTI JAVA (TRIVENETO, NEXI, ECC.)**
http.user_agent contains "Java" and ip.src.country eq "IT"

**ASN GOOGLE**
ip.src.asnum in {15169 396982}

**Bot Ufficiali - Crawler Google verificato**
cf.client.bot and http.user_agent contains "Google"

**Bot Ufficiali - Crawler Bing verificato**
cf.client.bot and http.user_agent contains "bingbot"

**Gestionale - Sincronizzazione Danea Easyfatt**
http.user_agent contains "DaneaEasyfatt"

**Monitoraggio - Uptime Kuma probe**
ip.src eq 49.12.69.209 and http.user_agent contains "Kuma"

**Estensioni Immagini / Media CDN**
ends_with(http.request.uri.path, ".jpg") or ends_with(http.request.uri.path, ".jpeg") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".gif") or ends_with(http.request.uri.path, ".svg") or ends_with(http.request.uri.path, ".ico") or ends_with(http.request.uri.path, ".avif")

**Path / Feed - Feed prodotti**
http.request.uri.path contains "feed"

**Path / Feed - Crawler / bot TrovaPrezzi**
http.request.uri.path contains "trovaprezzi"

**Path / Feed - Ricerca Doofinder**
http.request.uri.path contains "doofinder"

**Path / Sync - Connector eBay / Amazon M2E Pro**
http.request.uri.path contains "M2ePro"

---

### Tabella di Riepilogo

| Categoria | Condizione | Dettaglio / Note |
| :--- | :--- | :--- |
| **Doofinder** | `ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}` | Crawler Doofinder (EU, USA, ASIA) per indicizzazione catalogo |
| **Pagamenti** | `http.user_agent contains "Java" and ip.src.country eq "IT"` | Callback gateway bancari Java da IP italiano (es. Consorzio Triveneto, Nexi) |
| **ASN** | `ip.src.asnum in {15169 396982}` | ASN Google / Google Cloud |
| **Bot Ufficiali** | `cf.client.bot and http.user_agent contains "Google"` | Crawler Google verificato |
| **Bot Ufficiali** | `cf.client.bot and http.user_agent contains "bingbot"` | Crawler Bing verificato |
| **Gestionale** | `http.user_agent contains "DaneaEasyfatt"` | Sincronizzazione Danea Easyfatt |
| **Monitoraggio** | `ip.src eq 49.12.69.209 and http.user_agent contains "Kuma"` | Uptime Kuma probe |
| **File Statici** | `ends_with(http.request.uri.path, ".jpg") or ends_with(http.request.uri.path, ".jpeg") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".gif") or ends_with(http.request.uri.path, ".svg") or ends_with(http.request.uri.path, ".ico") or ends_with(http.request.uri.path, ".avif")` | Bypass per immagini e asset grafici |
| **Path / Feed** | `http.request.uri.path contains "feed"` | Feed prodotti |
| **Path / Feed** | `http.request.uri.path contains "trovaprezzi"` | Crawler / bot TrovaPrezzi |
| **Path / Feed** | `http.request.uri.path contains "doofinder"` | Ricerca Doofinder |
| **Path / Sync** | `http.request.uri.path contains "M2ePro"` | Connector eBay / Amazon M2E Pro |

---

### Espressione Completa (Cloudflare Expression Builder)

```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (cf.client.bot and http.user_agent contains "bingbot") or (http.user_agent contains "DaneaEasyfatt") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (ends_with(http.request.uri.path, ".jpg") or ends_with(http.request.uri.path, ".jpeg") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".gif") or ends_with(http.request.uri.path, ".svg") or ends_with(http.request.uri.path, ".ico") or ends_with(http.request.uri.path, ".avif")) or (http.request.uri.path contains "feed") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "M2ePro")
```
