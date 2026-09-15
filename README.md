# Cloudflare Rules

Raccolta modulare e documentazione delle regole Cloudflare (WAF Custom Rules, Blocco Nazioni, Cache Rules / FPC e Bypass) ottimizzate per i principali CMS ed e-commerce:

* **WooCommerce** (`woocommerce/`)
* **WordPress** (`wordpress/`)
* **Magento 1** (`magento1/`)
* **Magento 2** (`magento2/`)
* **PrestaShop** (`prestashop/`)

---

## 🏗️ Architettura del Progetto

Il repository segue un approccio **Infrastructure-as-Code modulare**:
I file Markdown di documentazione nelle cartelle dei CMS **vengono generati automaticamente** a partire da componenti JSON riutilizzabili.

```text
cloudflare-rules/
├── build.py                  # Script di compilazione Markdown
├── src/
│   ├── rules/
│   │   ├── waf/              # Regole WAF atomiche (doofinder.json, danea.json, ecc.)
│   │   └── cache/            # Componenti di cache (fpc-everything.json, bypass per CMS)
│   └── profiles/             # Profili CMS che richiamano i componenti (woocommerce.json, ecc.)
│
├── woocommerce/              # Markdown compilati pronti per la consultazione
├── wordpress/
├── magento1/
├── magento2/
└── prestashop/
```

---

## 🚀 Come Modificare o Aggiungere Regole

### 1. Aggiungere / modificare una regola WAF
Crea o modifica un file JSON in `src/rules/waf/<nome_regola>.json`:
```json
{
  "id": "mio-servizio",
  "name": "Mio Servizio - Descrizione",
  "category": "Integrazioni",
  "description": "Spiegazione di cosa fa questa regola e perché è in whitelist.",
  "expression": "http.user_agent contains \"MioBot\" and ip.src.country eq \"IT\"",
  "note": "Note brevi per la tabella riassuntiva"
}
```

### 2. Associare la regola a uno o più CMS
Apri i profili desiderati in `src/profiles/<cms>.json` e aggiungi l'ID della regola nell'array `whitelist`:
```json
{
  "platform": "woocommerce",
  "title": "WooCommerce",
  "waf": {
    "whitelist": [
      "doofinder",
      "google-bot",
      "mio-servizio"
    ]
  }
}
```

### 3. Ricompilare i file Markdown
Esegui semplicemente lo script di build:
```bash
python3 build.py
```
Tutti i file `WHITELIST.md`, `COUNTRY_BLOCK.md`, `FPC.md` verranno rigenerati all'istante con tabelle, intestazioni `####`, spiegazioni ed espressioni `or` complete.

---

## ⚡ Best Practice per le Cache Rules di Cloudflare

Nel motore **Cache Rules** di Cloudflare (`http_request_cache_settings`), **l'ultima regola che matcha ha la precedenza** (sovrascrive le precedenti).

L'ordine corretto di configurazione su Cloudflare è:
1. **Regola 1: `FPC (Cache Everything)`**
   * Metodi: `http.request.method in {"GET" "HEAD"}`
   * Azione: `Eligible for cache` (Cache Everything), Edge TTL 1 giorno, Browser TTL respect origin, ignore query string.
2. **Regola 2: `CACHE WHITELIST (Bypass Cache)`** *(sotto la regola 1)*
   * Condizione: percorsi dinamici del CMS (carrello, checkout, account, admin, API) e cookie di sessione attiva.
   * Azione: `Bypass cache` (`cache: false`).

---

## 🚀 Deploy Automatico su Cloudflare (`deploy.py`)

Puoi applicare direttamente le regole WAF e Cache su qualsiasi dominio Cloudflare via API senza doverle incollare a mano:

```bash
# Deploy completo (WAF + Cache) su un dominio
python3 deploy.py --zone elidelagenzia.com --profile wordpress

# Deploy su WooCommerce
python3 deploy.py --zone miostore.it --profile woocommerce

# Solo regole WAF o solo Cache
python3 deploy.py --zone miostore.it --profile prestashop --waf-only
python3 deploy.py --zone miostore.it --profile prestashop --cache-only

# Simulazione (dry-run) per vedere il JSON inviato a Cloudflare
python3 deploy.py --zone miostore.it --profile magento2 --dry-run
```

