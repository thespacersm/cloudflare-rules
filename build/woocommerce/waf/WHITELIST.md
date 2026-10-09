# WAF WHITELIST - WOOCOMMERCE

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
Crawler ufficiale Bingbot con verifica di autenticità gestita da Cloudflare Bot Management per l'indicizzazione SEO (con esclusione di catalogsearch per prevenire flood del motore di ricerca).
```text
cf.client.bot and http.user_agent contains "bingbot" and not http.request.uri.path contains "catalogsearch"
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

#### Certificati SSL - /.well-known/
Validazione dei certificati SSL (ACME / DCV): Let's Encrypt, Sectigo e altre CA chiamano da IP esteri i file sotto /.well-known/ per emettere e rinnovare i certificati. Senza whitelist VERIFYLIST li sfida e la validazione fallisce. Sbloccato a prescindere dall'user-agent, perche' ogni CA usa un UA diverso.
```text
starts_with(http.request.uri.path, "/.well-known/")
```

#### Estensioni Asset Statici (CSS, JS, Media)
Bypass delle regole di blocco per fogli di stile, script, asset grafici e file multimediali, garantendo il caricamento fluido delle risorse e l'assenza di blocchi CDN.
```text
http.request.uri.path.extension in {"jpg" "jpeg" "png" "webp" "gif" "svg" "ico" "avif" "bmp" "tif" "tiff" "css" "js"}
```

#### Path / Feed - Feed prodotti
Endpoint URL dedicati all'esportazione dei feed prodotti verso comparatori e aggregatori di vendita.
```text
http.request.uri.path contains "feed"
```

#### Path / Feed - Crawler / bot TrovaPrezzi
Richieste provenienti dai crawler e spider di TrovaPrezzi per la sincronizzazione dei prezzi e delle offerte.
```text
http.request.uri.path contains "trovaprezzi" or http.user_agent contains "PriceCrawlerBot"
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

#### WooCommerce REST API & Sync
Accesso alle REST API native di WooCommerce per sincronizzazioni esterne con app, gestionali e servizi terzi.
```text
http.user_agent contains "WooCommerce" or http.request.uri.path contains "/wp-json/wc/"
```

#### Automattic / Jetpack / WordPress.com
Rete e servizi cloud di Automattic (AS2635) per sincronizzazione Jetpack, backup, statistiche e CDN.
```text
(ip.src.asnum eq 2635) or (http.user_agent contains "Jetpack") or (http.user_agent contains "WordPress.com") or (http.request.uri.path contains "/wp-json/jetpack/")
```

#### Brevo (Sendinblue) WooCommerce
Integrazione ufficiale e webhook del plugin Brevo per l'invio di email transazionali e marketing automation.
```text
http.user_agent contains "Brevo-WC" or http.request.uri.path contains "/wp-json/sendinblue-woo/"
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

#### Sync / API - eShoppingAdvisor
Connettore eShoppingAdvisor che legge le API REST WooCommerce (es. /wp-json/wc/v3/orders) da server Hetzner in Finlandia. Ramo 1: IP osservati (204.168.196.0/24, 204.168.198.0/24) con qualsiasi UA, perche' usa anche UA da browser. Ramo 2: UA EsaCmsApiIntegrations dal /17 Hetzner 204.168.128.0/17, se ruotano gli IP. Senza whitelist il blocco per paese (VERIFYLIST) lo sfida e la sync fallisce con 403.
```text
(ip.src in {204.168.196.0/24 204.168.198.0/24} and starts_with(http.request.uri.path, "/wp-json/wc/")) or (http.user_agent contains "EsaCmsApiIntegrations" and ip.src in {204.168.128.0/17} and starts_with(http.request.uri.path, "/wp-json/wc/"))
```

#### Sync / API - AI Operations
Chiamate API del connettore AI Operations per l'integrazione con servizi esterni basati su intelligenza artificiale.
```text
ip.src eq 94.177.9.11 and starts_with(http.user_agent, "AI-Operations/")
```

#### Sync / API - Catchr
Connettore Catchr (reportistica/data connector) che legge le API WooCommerce da IP OVH dedicati. IP ufficiali comunicati da Catchr.
```text
ip.src in {141.95.207.193 54.37.80.17 147.135.136.178 147.135.137.18 147.135.137.31}
```

#### Gestionale - TheSpace Manage
Chiamate della piattaforma interna di gestione TheSpace Manage per operazioni amministrative sui siti clienti.
```text
ip.src eq 138.199.169.63 and starts_with(http.user_agent, "ThespaceManage/")
```

---

### Tabella di Riepilogo

| Categoria | Condizione | Dettaglio / Note |
| :--- | :--- | :--- |
| **Doofinder** | `ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}` | Crawler Doofinder (EU, USA, ASIA) per indicizzazione catalogo |
| **Pagamenti** | `http.user_agent contains "Java" and ip.src.country eq "IT"` | Callback gateway bancari Java da IP italiano (es. Consorzio Triveneto, Nexi) |
| **ASN** | `ip.src.asnum in {15169 396982}` | ASN Google / Google Cloud |
| **Bot Ufficiali** | `cf.client.bot and http.user_agent contains "Google"` | Crawler Google verificato |
| **Bot Ufficiali** | `cf.client.bot and http.user_agent contains "bingbot" and not http.request.uri.path contains "catalogsearch"` | Crawler Bing verificato (escluso catalogsearch) |
| **Gestionale** | `http.user_agent contains "DaneaEasyfatt"` | Sincronizzazione Danea Easyfatt |
| **Monitoraggio** | `ip.src eq 49.12.69.209 and http.user_agent contains "Kuma"` | Uptime Kuma probe |
| **Certificati** | `starts_with(http.request.uri.path, "/.well-known/")` | Tutto /.well-known/ (validazione certificati, qualsiasi CA) |
| **File Statici** | `http.request.uri.path.extension in {"jpg" "jpeg" "png" "webp" "gif" "svg" "ico" "avif" "bmp" "tif" "tiff" "css" "js"}` | Bypass per CSS, JS, immagini e asset statici |
| **Path / Feed** | `http.request.uri.path contains "feed"` | Feed prodotti |
| **Path / Feed** | `http.request.uri.path contains "trovaprezzi" or http.user_agent contains "PriceCrawlerBot"` | Crawler / bot TrovaPrezzi (path o User-Agent PriceCrawlerBot) |
| **Path / Feed** | `http.request.uri.path contains "doofinder"` | Ricerca Doofinder |
| **Path / Sync** | `http.request.uri.path contains "M2ePro"` | Connector eBay / Amazon M2E Pro |
| **WooCommerce API** | `http.user_agent contains "WooCommerce" or http.request.uri.path contains "/wp-json/wc/"` | Chiamate REST API WooCommerce |
| **Automattic / Jetpack** | `(ip.src.asnum eq 2635) or (http.user_agent contains "Jetpack") or (http.user_agent contains "WordPress.com") or (http.request.uri.path contains "/wp-json/jetpack/")` | Servizi e sincronizzazione Jetpack / WordPress.com (AS2635) |
| **Brevo / Email Marketing** | `http.user_agent contains "Brevo-WC" or http.request.uri.path contains "/wp-json/sendinblue-woo/"` | Integrazione e webhook Brevo WooCommerce |
| **Pagamenti** | `http.request.method eq "POST" and http.user_agent contains "PayPal" and (http.request.uri.path contains "paypal" or http.request.uri.query contains "paypal")` | Notifiche IPN e webhook PayPal (POST con User-Agent PayPal) |
| **Pagamenti** | `http.request.method eq "POST" and starts_with(http.user_agent, "Stripe/") and (http.request.uri.path contains "stripe" or http.request.uri.query contains "stripe")` | Webhook ufficiali Stripe (POST con User-Agent Stripe/) |
| **Pagamenti** | `http.request.method eq "POST" and ip.src.country in {"SM" "IT"} and http.request.uri.path contains "bkn"` | Notifiche server BKN301 (POST da IT/SM) |
| **Sync / API** | `(ip.src in {204.168.196.0/24 204.168.198.0/24} and starts_with(http.request.uri.path, "/wp-json/wc/")) or (http.user_agent contains "EsaCmsApiIntegrations" and ip.src in {204.168.128.0/17} and starts_with(http.request.uri.path, "/wp-json/wc/"))` | eShoppingAdvisor su API WooCommerce (IP /24 osservati, oppure UA nel /17 Hetzner) |
| **Sync / API** | `ip.src eq 94.177.9.11 and starts_with(http.user_agent, "AI-Operations/")` | Connettore AI Operations (IP + User-Agent dedicati, nessun vincolo di path) |
| **Sync / API** | `ip.src in {141.95.207.193 54.37.80.17 147.135.136.178 147.135.137.18 147.135.137.31}` | IP ufficiali Catchr |
| **Gestionale** | `ip.src eq 138.199.169.63 and starts_with(http.user_agent, "ThespaceManage/")` | Connettore TheSpace Manage (IP + User-Agent dedicati) |

---

### Espressione Completa (Cloudflare Expression Builder)

```text
(ip.src in {54.171.4.216 52.2.218.41 18.143.220.25}) or (http.user_agent contains "Java" and ip.src.country eq "IT") or (ip.src.asnum in {15169 396982}) or (cf.client.bot and http.user_agent contains "Google") or (cf.client.bot and http.user_agent contains "bingbot" and not http.request.uri.path contains "catalogsearch") or (http.user_agent contains "DaneaEasyfatt") or (ip.src eq 49.12.69.209 and http.user_agent contains "Kuma") or (starts_with(http.request.uri.path, "/.well-known/")) or (http.request.uri.path.extension in {"jpg" "jpeg" "png" "webp" "gif" "svg" "ico" "avif" "bmp" "tif" "tiff" "css" "js"}) or (http.request.uri.path contains "feed") or (http.request.uri.path contains "trovaprezzi" or http.user_agent contains "PriceCrawlerBot") or (http.request.uri.path contains "doofinder") or (http.request.uri.path contains "M2ePro") or (http.user_agent contains "WooCommerce" or http.request.uri.path contains "/wp-json/wc/") or ((ip.src.asnum eq 2635) or (http.user_agent contains "Jetpack") or (http.user_agent contains "WordPress.com") or (http.request.uri.path contains "/wp-json/jetpack/")) or (http.user_agent contains "Brevo-WC" or http.request.uri.path contains "/wp-json/sendinblue-woo/") or (http.request.method eq "POST" and http.user_agent contains "PayPal" and (http.request.uri.path contains "paypal" or http.request.uri.query contains "paypal")) or (http.request.method eq "POST" and starts_with(http.user_agent, "Stripe/") and (http.request.uri.path contains "stripe" or http.request.uri.query contains "stripe")) or (http.request.method eq "POST" and ip.src.country in {"SM" "IT"} and http.request.uri.path contains "bkn") or ((ip.src in {204.168.196.0/24 204.168.198.0/24} and starts_with(http.request.uri.path, "/wp-json/wc/")) or (http.user_agent contains "EsaCmsApiIntegrations" and ip.src in {204.168.128.0/17} and starts_with(http.request.uri.path, "/wp-json/wc/"))) or (ip.src eq 94.177.9.11 and starts_with(http.user_agent, "AI-Operations/")) or (ip.src in {141.95.207.193 54.37.80.17 147.135.136.178 147.135.137.18 147.135.137.31}) or (ip.src eq 138.199.169.63 and starts_with(http.user_agent, "ThespaceManage/"))
```
