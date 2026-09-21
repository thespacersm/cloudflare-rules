# WAF WHITELIST - MAGENTO 1

### Azione
`Skip`
- Skip all remaining rules in current ruleset
- Phase: `http_ratelimit`, `http_request_firewall_managed`, `http_request_sbfm`
- Products: `WAF`, `Rate Limiting`, `Security Level`, `Zone Lockdown`, `User Agent Blocking`, `Browser Integrity Check`

---

### Regole e Condizioni con Commenti

#### DOOFINDER CRAWLER (IP EU, USA, ASIA)
Indirizzi IP ufficiali dei server e crawler Doofinder utilizzati per scaricare il catalogo e indicizzare i prodotti nella barra di ricerca.
```text
ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}
```

#### PAGAMENTI JAVA (TRIVENETO, NEXI, ECC.)
Chiamate di notifica/callback server-to-server dei gateway di pagamento bancari (es. Consorzio Triveneto, Nexi) effettuate tramite client Java da IP italiano.
```text
http.user_agent contains "Java" and ip.src.country eq "IT"
```

#### ASN GOOGLE
Autonomous System Numbers (ASN) di Google e Google Cloud per garantire l'accesso a servizi, crawler e API di Google.
```text
ip.src.asnum in {15169 396982}
```

#### Bot Ufficiali - Crawler Google verificato
Crawler ufficiale Googlebot con verifica di autenticità gestita da Cloudflare Bot Management per l'indicizzazione SEO.
```text
cf.client.bot and http.user_agent contains "Google"
```

#### Bot Ufficiali - Crawler Bing verificato
Crawler ufficiale Bingbot con verifica di autenticità gestita da Cloudflare Bot Management per l'indicizzazione SEO.
```text
cf.client.bot and http.user_agent contains "bingbot"
```

#### Gestionale - Sincronizzazione Danea Easyfatt
Chiamate del software gestionale Danea Easyfatt per l'aggiornamento automatico di catalogo, ordini e giacenze.
```text
http.user_agent contains "DaneaEasyfatt"
```

#### Monitoraggio - Uptime Kuma probe
Sonda di monitoraggio Uptime Kuma per il controllo costante di disponibilità del sito e stato del server.
```text
ip.src eq 49.12.69.209 and http.user_agent contains "Kuma"
```

#### Estensioni Immagini / Media CDN
Bypass delle regole di blocco per asset grafici e file multimediali, evitando blocchi CDN o anteprime corrotte da server esterni.
```text
ends_with(http.request.uri.path, ".jpg") or ends_with(http.request.uri.path, ".jpeg") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".gif") or ends_with(http.request.uri.path, ".svg") or ends_with(http.request.uri.path, ".ico") or ends_with(http.request.uri.path, ".avif")
```

#### Path / Feed - Feed prodotti
Endpoint URL dedicati all'esportazione dei feed prodotti verso comparatori e aggregatori di vendita.
```text
http.request.uri.path contains "feed"
```

#### Path / Feed - Crawler / bot TrovaPrezzi
Richieste provenienti dai crawler e spider di TrovaPrezzi per la sincronizzazione dei prezzi e delle offerte.
```text
http.request.uri.path contains "trovaprezzi"
```

#### Path / Feed - Ricerca Doofinder
Richieste verso endpoint di ricerca o feed specifici dedicati a Doofinder.
```text
http.request.uri.path contains "doofinder"
```

#### Path / Sync - Connector eBay / Amazon M2E Pro
Chiamate API del connettore M2E Pro per la sincronizzazione dei marketplace Amazon ed eBay.
```text
http.request.uri.path contains "M2ePro"
```

#### Sync / API - Connettore Windsor.ai
Chiamate API REST del connettore Windsor.ai per sincronizzazione dati e reportistica BI.
```text
http.request.uri.path contains "/rest/" and http.user_agent eq "Windsor/1.0"
```

#### PayPal - IPN & Webhook di Pagamento
Chiamate POST di notifica IPN e Webhook REST inviate dai server PayPal con User-Agent proprietario.
```text
http.request.method eq "POST" and http.user_agent contains "PayPal" and (http.request.uri.path contains "paypal" or http.request.uri.query contains "paypal")
```

#### Stripe - Webhook di Pagamento
Notifiche webhook server-to-server inviate dai server Stripe con User-Agent ufficiale in formato POST.
```text
http.request.method eq "POST" and starts_with(http.user_agent, "Stripe/") and (http.request.uri.path contains "stripe" or http.request.uri.query contains "stripe")
```

#### BKN301 - Notifiche Gateway Bancario
Notifiche server-to-server di conferma transazione dai gateway BKN301 (Banca di San Marino) inviate via POST da IP italiani o sammarinesi.
```text
http.request.method eq "POST" and ip.src.country in {"SM" "IT"} and http.request.uri.path contains "bkn"
```

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
| **Sync / API** | `http.request.uri.path contains "/rest/" and http.user_agent eq "Windsor/1.0"` | Connettore REST Windsor.ai |
| **Pagamenti** | `http.request.method eq "POST" and http.user_agent contains "PayPal" and (http.request.uri.path contains "paypal" or http.request.uri.query contains "paypal")` | Notifiche IPN e webhook PayPal (POST con User-Agent PayPal) |
| **Pagamenti** | `http.request.method eq "POST" and starts_with(http.user_agent, "Stripe/") and (http.request.uri.path contains "stripe" or http.request.uri.query contains "stripe")` | Webhook ufficiali Stripe (POST con User-Agent Stripe/) |
| **Pagamenti** | `http.request.method eq "POST" and ip.src.country in {"SM" "IT"} and http.request.uri.path contains "bkn"` | Notifiche server BKN301 (POST da IT/SM) |

---

### Espressione Completa (Cloudflare Expression Builder)

```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (cf.client.bot and http.user_agent contains "bingbot") or (http.user_agent contains "DaneaEasyfatt") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (ends_with(http.request.uri.path, ".jpg") or ends_with(http.request.uri.path, ".jpeg") or ends_with(http.request.uri.path, ".png") or ends_with(http.request.uri.path, ".webp") or ends_with(http.request.uri.path, ".gif") or ends_with(http.request.uri.path, ".svg") or ends_with(http.request.uri.path, ".ico") or ends_with(http.request.uri.path, ".avif")) or (http.request.uri.path contains "feed") or (http.request.uri.path contains "trovaprezzi") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "M2ePro") or (http.request.uri.path contains "/rest/" and http.user_agent eq "Windsor/1.0") or (http.request.method eq "POST" and http.user_agent contains "PayPal" and (http.request.uri.path contains "paypal" or http.request.uri.query contains "paypal")) or (http.request.method eq "POST" and starts_with(http.user_agent, "Stripe/") and (http.request.uri.path contains "stripe" or http.request.uri.query contains "stripe")) or (http.request.method eq "POST" and ip.src.country in {"SM" "IT"} and http.request.uri.path contains "bkn")
```
