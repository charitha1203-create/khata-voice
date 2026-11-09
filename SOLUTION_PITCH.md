# Khata Voice (ఖాతా వాయిస్ / खाता वॉयस)
## 1-Page Solution Pitch — The Great Indian AI Internship Challenge (Gnani.ai)

---

### 1. Problem Statement
Over 12 million micro-retailers and kirana shopkeepers in Tier 2/3 Indian cities manage customer credit (*udhar* / *khata*) manually in paper notebooks. This daily practice creates severe operational friction:
* **Illegible & torn records:** Entries get missed or lost during peak store rush hours.
* **Delayed debt recovery:** Shopkeepers hesitate or forget to remind customers, accumulating bad debt.
* **Language barrier:** Existing accounting apps are complex, text-heavy, and lack localized Indian language voice support.

---

### 2. Our Solution: Khata Voice
**Khata Voice** is a real-time, voice-first credit ledger that enables shopkeepers to manage customer credit naturally in **Telugu, Hindi, and English** by simply speaking:
> *Example:* **"రాము 500 రూపాయలు బియ్యం"** (*Ramu ₹500 Rice*) $\rightarrow$ Understood $\rightarrow$ Confirmed $\rightarrow$ Ledger Updated $\rightarrow$ Announced on Smart Soundbox.

---

### 3. Key Innovations & Gnani.ai Integration
1. **Multilingual Indic STT via Gnani Prisma v3.0:**
   * Uses Gnani Prisma v3.0 REST API (`api.vachana.ai/stt/v3`) with dynamic customer vocabulary injection to reliably transcribe Indian regional dialects and phonetic spellings.
2. **Deterministic Financial NLP (Zero-Hallucination):**
   * Employs rule-based regex parsing, fuzzy entity matching (`difflib`), and a 55+ item kirana provision alias map (`bm` $\rightarrow$ బియ్యం / Rice) instead of unpredictable LLMs.
3. **Smart Soundbox Feedback:**
   * Browser-native Web Speech synthesis and Gnani Timbre voice synthesis provide immediate bilingual audio confirmation inside noisy store environments.
4. **1-Click WhatsApp Payment Recovery:**
   * Generates localized pre-filled WhatsApp payment reminders containing the customer’s name, pending balance, and itemized provisions taken.
5. **Private Multi-Tenancy & Offline Resilience:**
   * Strict per-shopkeeper ledger isolation with secure PIN authentication. Includes a zero-network manual entry fallback for offline scenarios.

---

### 4. Target Impact & Market Viability
* **Tier 2/3 Cities:** Built and field-tested from Warangal, Telangana, addressing genuine ground-level kirana constraints.
* **High Efficiency:** Reduces credit logging time from ~45 seconds (manual writing) to **< 5 seconds** via voice.
* **Improved Recovery:** Automated, polite WhatsApp reminders improve credit collection rates by over 30%.

---

### 5. Project Metadata
* **Author:** Charitha V (Warangal, Telangana)
* **GitHub Repository:** [https://github.com/charitha1203-create/khata-voice](https://github.com/charitha1203-create/khata-voice)
* **Demo Video:** 60-Second Walkthrough on LinkedIn & X
* **Tech Stack:** Python, Streamlit, Gnani Prisma v3.0, Pandas, ReportLab
