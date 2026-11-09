# 🎙️ Khata Voice (ఖాతా వాయిస్ / खाता वॉयस)

> **Multilingual Real-Time Voice Ledger for Indian Kirana & Retail Shopkeepers**  
> Built for the **Gnani.ai Great Indian AI Internship Challenge**  
> Powered by **Gnani Prisma v3.0 STT**

---

## 🌟 What is Khata Voice?

Khata Voice lets shopkeepers manage customer credit (udhar/khata) using **natural voice commands** in Telugu, Hindi, or English — no typing needed. It's built for small kirana shops and general stores in Tier 2/3 cities like Warangal, Telangana.

**Say:** `"రాము 500 రూపాయలు బియ్యం"` (Ramu 500 rupees rice)  
**Khata Voice:** Understands → Confirms → Saves to ledger → Announces via Soundbox 🔊

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎙️ **Voice Entry** | Speak in Telugu / Hindi / English — Gnani Prisma STT transcribes it |
| 🔊 **Smart Soundbox** | Auto-announces every transaction in the shopkeeper's language |
| 📒 **Multi-Tenant Ledger** | Every shopkeeper has a private, isolated account |
| 📲 **WhatsApp Reminders** | 1-click pre-filled reminder to customer with exact balance |
| ✍️ **Manual Entry** | Add entries via keyboard — works 100% offline |
| 👤 **Customer Drill-Down** | Full transaction history per customer with running balance |
| 📅 **Date Range Filter** | Filter history by date range or customer |
| 📈 **Monthly Trend Chart** | Credit vs. payments received line chart |
| ↩️ **Undo Last Entry** | Two-step confirmation delete for accidental entries |
| 🔍 **Quick Balance Lookup** | Instant balance for any customer |
| 🌐 **Trilingual UI** | Full Telugu / Hindi / English localization |
| 🔐 **PIN-Based Auth** | Secure shopkeeper login with per-language preference |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (Python) |
| **STT** | Gnani Prisma v3.0 REST API (`api.vachana.ai/stt/v3`) |
| **TTS / Soundbox** | Web Speech API (browser-native, zero dependency) |
| **NLP** | Deterministic regex + difflib fuzzy matching (no LLM hallucinations) |
| **Storage** | JSON files per shopkeeper (portable, no DB setup) |
| **Languages** | Telugu (te-IN), Hindi (hi-IN), English (en-IN) |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install streamlit pandas python-dotenv requests
```

### 2. Set your Gnani API key
Create a `.env` file in the project root:
```
GNANI_API_KEY=your_gnani_api_key_here
```

### 3. Run the app
```bash
python -m streamlit run app.py
```

### 4. Demo login
- **Username:** `chari` | **PIN:** `1234` (pre-loaded with demo entries)

---

## 📁 Project Structure

```
khata-voice/
├── app.py              # Main Streamlit app (UI + auth + all tabs)
├── pipeline.py         # Propose / confirm flow
├── intent.py           # 4-intent classifier (add/ask/pay/correct)
├── extract.py          # Entity extractor (customer, amount, provision)
├── ledger.py           # Multi-tenant ledger operations
├── stt.py              # Gnani Prisma v3.0 STT client
├── tts.py              # Soundbox HTML + WhatsApp link generator
├── auth.py             # PIN auth, user registration
├── build_pdf_report.py # Generates 15-page PDF project report
└── .env                # (not committed) GNANI_API_KEY=...
```

---

## 🎯 Provision Alias Support

Shopkeepers can say shorthand — Khata Voice understands:

| Said | Understood As |
|---|---|
| `bm` | బియ్యం (Rice) |
| `nune` | నూనె (Oil) |
| `panchadar` | పంచదార (Sugar) |
| `aata` | గోధుమ పిండి (Wheat Flour) |
| `sabbu` | సబ్బు (Soap) |
| `tea` | టీ పొడి (Tea Powder) |

---

## 🏆 Awards Targeted

- 🥇 **Regional Language Excellence** — Full Telugu + Hindi STT + UI
- 🥈 **Tier 2/3 City Impact** — Built in and for Warangal, Telangana
- 🥉 **60-Second Demo** — Concise demo video ≤60 seconds
- 🎖️ **Real-World Impact** — Solves actual daily pain of kirana shopkeepers

---

## 👨‍💻 Author

**Charitha** | Warangal, Telangana  
Built for: *Gnani.ai Great Indian AI Internship Challenge*
