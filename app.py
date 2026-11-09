import os
import importlib
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import date, datetime
from dotenv import load_dotenv

import pipeline
import ledger
import auth
import tts

# Force-reload modules on every rerun so no stale in-memory module state is ever used
importlib.reload(ledger)
importlib.reload(pipeline)
importlib.reload(auth)
importlib.reload(tts)

load_dotenv()

st.set_page_config(page_title="Khata Voice — Voice Ledger", page_icon="🎙️", layout="wide")

# --- I18N DICTIONARY FOR LOCALIZATION ---
I18N = {
    "te": {
        "app_title": "🎙️ ఖాతా వాయిస్ (Khata Voice)",
        "app_subtitle": "చిరు వ్యాపారుల రియల్-టైమ్ వాయిస్ లెడ్జర్ (కిరాణా & జనరల్ స్టోర్స్)",
        "outstanding": "మొత్తం బాకీ (Outstanding)",
        "active_cust": "ఖాతాదారులు (బాకీ ఉన్నవారు)",
        "settled_cust": "క్లియర్ అయిన ఖాతాలు (Settled)",
        "step1_title": "1. వాయిస్ రికార్డ్ చేయండి లేదా ఆడియో అప్‌లోడ్ చేయండి",
        "record_hint": "ఎంట్రీ మాట్లాడండి (30 సెకన్ల లోపు)",
        "or_upload": "లేదా ఆడియో ఫైల్ అప్‌లోడ్ చేయండి",
        "btn_transcribe": "🎙️ వాయిస్ అర్థం చేసుకోండి",
        "step2_title": "2. ఎంట్రీని తనిఖీ చేసి ధృవీకరించండి",
        "heard": "వినబడిన మాటలు:",
        "intent": "గుర్తించిన ఉద్దేశం:",
        "lang": "భాష:",
        "customer": "ఖాతాదారు:",
        "amount": "మొత్తం:",
        "provision": "సరుకు:",
        "btn_confirm": "✅ లెడ్జర్‌లో నమోదు చేయండి (Confirm)",
        "btn_cancel": "❌ రద్దు చేయండి (Cancel)",
        "step3_title": "3. ఈ దుకాణం ఖాతా పుస్తకం (Shop Ledger)",
        "tab_balances": "ఖాతాదారులు & సరుకులు (Balances)",
        "tab_history": "పూర్తి లావాదేవీల చరిత్ర (History)",
        "tab_analytics": "📊 దుకాణ విశ్లేషణ (Analytics)",
        "tab_manual": "✍️ చేతితో ఎంట్రీ (Manual Entry)",
        "col_customer": "ఖాతాదారు (Customer)",
        "col_balance": "బాకీ ₹ (Balance)",
        "col_provisions": "తీసుకున్న సరుకులు (Provisions)",
        "col_status": "స్థితి (Status)",
        "btn_export": "📥 లెడ్జర్ CSV డౌన్‌లోడ్ చేయండి",
        "status_owes": "బాకీ (Owes)",
        "status_settled": "క్లియర్ (Settled)",
        "status_advance": "అడ్వాన్స్ (Advance)",
        "quick_demo": "⚡ త్వరిత డెమో నమూనాలు",
        "shop_customers_title": "👥 ఈ దుకాణం ఖాతాదారులు (Your Customers)",
        "no_customers": "ఇంకా ఖాతాదారులు లేరు (No customers yet)",
        "logout": "లాగౌట్ (Log Out)",
        "switch_lang": "భాషను మార్చండి (Language)",
        "empty_ledger": "ఈ దుకాణంలో ఇంకా ఎలాంటి ఎంట్రీలు నమోదు కాలేదు. పైన వాయిస్ మాట్లాడి రికార్డ్ చేయండి!",
        "search_label": "🔍 ఖాతాదారు లేదా సరుకు పేరు వెతకండి (Search)",
        "send_whatsapp": "📲 WhatsApp రిమైండర్ పంపండి",
        "total_credit": "మొత్తం ఇచ్చిన అప్పు (Total Credit)",
        "total_collected": "వసూలు అయిన నగదు (Collected)",
        "recovery_rate": "రికవరీ రేటు (Recovery Rate)",
        "top_debtors_title": "అత్యధిక బాకీ ఉన్న ఖాతాదారులు",
        "top_provisions_title": "అత్యధికంగా అమ్ముడైన సరుకులు",
        "manual_entry_title": "✍️ చేతితో ఎంట్రీ నమోదు చేయండి (Add Entry Manually)",
        "manual_name": "ఖాతాదారు పేరు (Customer Name)",
        "manual_amount": "మొత్తం రూపాయలు (Amount ₹)",
        "manual_provision": "సరుకు (Provision)",
        "manual_type": "ఎంట్రీ రకం (Entry Type)",
        "manual_btn_add": "➕ ఖాతాలో చేర్చండి (Add to Khata)",
        "manual_btn_pay": "💳 చెల్లింపు నమోదు (Record Payment)",
        "quick_lookup": "🔍 తక్షణ బాకీ చూడండి (Quick Balance Lookup)",
        "undo_last": "↩️ చివరి ఎంట్రీ తొలగించండి (Undo Last Entry)",
        "trend_title": "📈 నెలవారీ అప్పు ట్రెండ్ (Monthly Credit Trend)",
        "customer_detail": "👤 ఖాతాదారు వివరాలు (Customer Detail)",
        "total_entries": "మొత్తం లావాదేవీలు (Total Entries)",
    },
    "hi": {
        "app_title": "🎙️ खाता वॉयस (Khata Voice)",
        "app_subtitle": "दुकानदारों के लिए रियल-टाइम वॉयस बही-खाता (किराना और जनरल स्टोर)",
        "outstanding": "कुल बाकी उधार (Outstanding)",
        "active_cust": "सक्रिय ग्राहक (उधार वाले)",
        "settled_cust": "हिसाब चुकता (Settled)",
        "step1_title": "1. बोलकर या ऑडियो अपलोड करके रिकॉर्ड करें",
        "record_hint": "एंट्री बोलें (30 सेकंड के अंदर)",
        "or_upload": "या ऑडियो फ़ाइल अपलोड करें",
        "btn_transcribe": "🎙️ आवाज़ को समझें (Transcribe)",
        "step2_title": "2. एंट्री की जांच करें और पुष्टि करें",
        "heard": "सुना गया:",
        "intent": "पहचाना गया उद्देश्य:",
        "lang": "भाषा:",
        "customer": "ग्राहक:",
        "amount": "रुपये:",
        "provision": "सामान / राशन:",
        "btn_confirm": "✅ खाते में दर्ज करें (Confirm)",
        "btn_cancel": "❌ रद्द करें (Cancel)",
        "step3_title": "3. इस दुकान का बही-खाता (Shop Ledger)",
        "tab_balances": "ग्राहकों का हिसाब और राशन (Balances)",
        "tab_history": "लेन-देन का पूरा इतिहास (History)",
        "tab_analytics": "📊 दुकान का विश्लेषण (Analytics)",
        "tab_manual": "✍️ हाथ से दर्ज करें (Manual Entry)",
        "col_customer": "ग्राहक (Customer)",
        "col_balance": "बाकी रुपये ₹ (Balance)",
        "col_provisions": "सामान / राशन (Provisions)",
        "col_status": "स्थिति (Status)",
        "btn_export": "📥 बही-खाता CSV डाउनलोड करें",
        "status_owes": "बाकी (Owes)",
        "status_settled": "चुकता (Settled)",
        "status_advance": "जमा (Advance)",
        "quick_demo": "⚡ तुरंत डेमो के उदाहरण",
        "shop_customers_title": "👥 इस दुकान के ग्राहक (Your Customers)",
        "no_customers": "अभी कोई ग्राहक नहीं है (No customers yet)",
        "logout": "लॉग आउट (Log Out)",
        "switch_lang": "भाषा बदलें (Language)",
        "empty_ledger": "इस दुकान में अभी कोई एंट्री दर्ज नहीं है। ऊपर बोलकर रिकॉर्ड करें!",
        "search_label": "🔍 ग्राहक या सामान का नाम खोजें (Search)",
        "send_whatsapp": "📲 WhatsApp तकादा / रिमाइंडर भेजें",
        "total_credit": "कुल दिया गया उधार (Total Credit)",
        "total_collected": "कुल वसूल हुआ पैसा (Collected)",
        "recovery_rate": "वसूली दर (Recovery Rate)",
        "top_debtors_title": "सबसे ज्यादा बाकी वाले ग्राहक",
        "top_provisions_title": "सबसे ज्यादा बिकने वाला सामान",
        "manual_entry_title": "✍️ हाथ से एंट्री दर्ज करें (Add Entry Manually)",
        "manual_name": "ग्राहक का नाम (Customer Name)",
        "manual_amount": "रुपये की राशि (Amount ₹)",
        "manual_provision": "सामान (Provision)",
        "manual_type": "एंट्री का प्रकार (Entry Type)",
        "manual_btn_add": "➕ खाते में जोड़ें (Add to Khata)",
        "manual_btn_pay": "💳 भुगतान दर्ज करें (Record Payment)",
        "quick_lookup": "🔍 तुरंत बाकी देखें (Quick Balance Lookup)",
        "undo_last": "↩️ अंतिम एंट्री हटाएं (Undo Last Entry)",
        "trend_title": "📈 मासिक उधार ट्रेंड (Monthly Credit Trend)",
        "customer_detail": "👤 ग्राहक विवरण (Customer Detail)",
        "total_entries": "कुल लेन-देन (Total Entries)",
    },
    "en": {
        "app_title": "🎙️ Khata Voice",
        "app_subtitle": "Multilingual Real-Time Voice Ledger for Kirana & Retail Stores",
        "outstanding": "Total Outstanding",
        "active_cust": "Active Customers with Balance",
        "settled_cust": "Settled Accounts",
        "step1_title": "1. Speak or Upload Audio",
        "record_hint": "Record an entry (under 30 seconds)",
        "or_upload": "Or upload an audio clip",
        "btn_transcribe": "🎙️ Transcribe & Understand Voice",
        "step2_title": "2. Review & Confirm Entry",
        "heard": "Heard:",
        "intent": "Detected Intent:",
        "lang": "Language:",
        "customer": "Customer:",
        "amount": "Amount:",
        "provision": "Provision:",
        "btn_confirm": "✅ Confirm & Save to Khata",
        "btn_cancel": "❌ Cancel",
        "step3_title": "3. This Shop's Ledger",
        "tab_balances": "Customer Balances & Provisions",
        "tab_history": "Transaction History",
        "tab_analytics": "📊 Kirana Analytics",
        "tab_manual": "✍️ Manual Entry",
        "col_customer": "Customer",
        "col_balance": "Balance (₹)",
        "col_provisions": "Provisions Taken",
        "col_status": "Status",
        "btn_export": "📥 Export Ledger to CSV",
        "status_owes": "Owes",
        "status_settled": "Settled",
        "status_advance": "Advance",
        "quick_demo": "⚡ Quick Demo / Test Phrases",
        "shop_customers_title": "👥 This Shop's Customers",
        "no_customers": "No customers registered yet",
        "logout": "Log Out",
        "switch_lang": "Language",
        "empty_ledger": "No entries recorded yet for this shop. Record a voice note above or click a demo sample on the sidebar!",
        "search_label": "🔍 Search customer or provision name",
        "send_whatsapp": "📲 Send WhatsApp Reminder",
        "total_credit": "Total Credit Given",
        "total_collected": "Total Debt Recovered",
        "recovery_rate": "Debt Recovery Rate",
        "top_debtors_title": "Top Customers by Outstanding Debt",
        "top_provisions_title": "Most Demanded Provisions",
        "manual_entry_title": "✍️ Add Entry Manually (No Mic Needed)",
        "manual_name": "Customer Name",
        "manual_amount": "Amount (₹)",
        "manual_provision": "Provision / Item",
        "manual_type": "Entry Type",
        "manual_btn_add": "➕ Add Credit to Khata",
        "manual_btn_pay": "💳 Record Payment",
        "quick_lookup": "🔍 Quick Balance Lookup",
        "undo_last": "↩️ Undo Last Entry",
        "trend_title": "📈 Monthly Credit Trend",
        "customer_detail": "👤 Customer Detail View",
        "total_entries": "Total Entries",
    }
}

# Common kirana provisions list (for manual entry dropdown)
PROVISION_LIST = [
    "— (Cash Credit / No Item)",
    "బియ్యం (Rice)",
    "పంచదార (Sugar)",
    "నూనె (Oil)",
    "కందిపప్పు (Dal)",
    "గోధుమ పిండి (Aata/Wheat Flour)",
    "సబ్బు (Soap)",
    "టీ పొడి (Tea Powder)",
    "కాఫీ (Coffee)",
    "ఉప్పు (Salt)",
    "మిర్చి పొడి (Chilli Powder)",
    "పసుపు (Turmeric)",
    "మసాలా (Masala)",
    "బిస్కెట్లు (Biscuits)",
    "నూడుల్స్ (Noodles)",
    "పాలు (Milk)",
    "చక్కెర (Jaggery)",
    "కొబ్బరి నూనె (Coconut Oil)",
    "సన్‌ఫ్లవర్ ఆయిల్ (Sunflower Oil)",
    "Other",
]

# --- AUTHENTICATION GATEWAY ---
if "user" not in st.session_state:
    st.session_state["user"] = None

user = st.session_state["user"]

# If user is not logged in, show Sign In / Sign Up portal
if user is None:
    st.title("🎙️ Khata Voice (ఖాతా వాయిస్ / खाता वॉयस)")
    st.caption("Powered by **Gnani.ai Prisma v3.0** | The Great Indian AI Internship Challenge")
    st.markdown("---")

    col_auth_left, col_auth_right = st.columns([1.2, 1])

    with col_auth_left:
        st.subheader("🏪 Welcome to Khata Voice")
        st.write(
            "Every shopkeeper has their own private, independent khata ledger. "
            "Customer details and credit entries belong exclusively to that shopkeeper and are never visible to any other shop."
        )
        st.info("💡 **Instant Demo Access:** A pre-configured shopkeeper account is ready. Just click below!")
        if st.button("🚀 Quick Demo Login as Chari (శ్రీ లక్ష్మి కిరాణా — తెలుగు)", type="primary"):
            ok, demo_u, msg = auth.authenticate_user("chari", "1234")
            if ok:
                st.session_state.clear()
                st.session_state["user"] = demo_u
                st.rerun()

    with col_auth_right:
        auth_tab_login, auth_tab_signup = st.tabs(["🔑 లాగిన్ (Login)", "📝 కొత్త ఖాతా (Sign Up)"])

        with auth_tab_login:
            st.markdown("#### దుకాణదారు లాగిన్ (Shopkeeper Login)")
            login_user = st.text_input("ఖాతా పేరు / Username", value="chari", key="l_user")
            login_pin = st.text_input("4-అంకెల పిన్ / PIN", value="1234", type="password", key="l_pin")

            if st.button("ప్రవేశించండి / Sign In", key="btn_signin"):
                ok, auth_user, msg = auth.authenticate_user(login_user, login_pin)
                if ok:
                    st.session_state.clear()
                    st.session_state["user"] = auth_user
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab_signup:
            st.markdown("#### కొత్త దుకాణం నమోదు (Create Account)")
            s_shop = st.text_input("దుకాణం పేరు (Shop Name)", placeholder="ఉదా: శ్రీ బాలాజీ కిరాణా స్టోర్స్", key="s_shop")
            s_owner = st.text_input("యజమాని పేరు (Owner Name)", placeholder="ఉదా: రాకేష్", key="s_owner")
            s_user = st.text_input("యూజర్‌నేమ్ (Username / ID)", placeholder="ఉదా: rakesh_kirana", key="s_user")
            s_pin = st.text_input("4-అంకెల సెక్యూరిటీ పిన్ (PIN)", type="password", placeholder="కనీసం 4 అంకెలు", key="s_pin")

            s_lang = st.radio(
                "మీ ప్రాధాన్య భాషను ఎంచుకోండి (Choose Default Language):",
                options=["te", "hi", "en"],
                format_func=lambda x: {"te": "తెలుగు (Telugu)", "hi": "हिंदी (Hindi)", "en": "English"}[x],
                key="s_lang"
            )

            if st.button("ఖాతాను సృష్టించండి / Create Account", key="btn_signup"):
                if not s_user.strip() or not s_pin.strip():
                    st.error("Please enter Username and PIN.")
                else:
                    ok, msg = auth.register_user(s_user, s_shop, s_owner, s_pin, s_lang)
                    if ok:
                        st.success(msg)
                        # Ensure empty ledger file exists strictly for this new user
                        ledger.save_entries([], s_user.strip().lower())
                        _, new_user, _ = auth.authenticate_user(s_user, s_pin)
                        st.session_state.clear()
                        st.session_state["user"] = new_user
                        st.rerun()
                    else:
                        st.error(msg)

else:
    # --- USER IS LOGGED IN ---
    current_username = user["username"]

    # Language resolution
    current_lang = user.get("language", "te")
    if current_lang not in I18N:
        current_lang = "te"
    T = I18N[current_lang]

    # --- SIDEBAR CONFIGURATION ---
    st.sidebar.title("🏪 " + user.get("shop_name", "Shop"))
    st.sidebar.caption(f"👤 ఖాతాదారు (Owner): **{user.get('owner_name', user['username'])}**")
    st.sidebar.caption(f"🆔 Shop ID: `{current_username}`")

    # Language Switcher
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🌐 {T['switch_lang']}")
    lang_options = ["te", "hi", "en"]
    lang_labels = {"te": "తెలుగు (Telugu)", "hi": "हिंदी (Hindi)", "en": "English"}

    selected_lang = st.sidebar.selectbox(
        "Select Language",
        options=lang_options,
        index=lang_options.index(current_lang),
        format_func=lambda x: lang_labels[x],
        label_visibility="collapsed"
    )

    if selected_lang != current_lang:
        auth.update_language(current_username, selected_lang)
        user["language"] = selected_lang
        st.session_state["user"] = user
        st.rerun()

    # Logout Button
    if st.sidebar.button(f"🚪 {T['logout']}", type="secondary"):
        st.session_state.clear()
        st.rerun()

    # Display ONLY this shop's registered customers in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"{T['shop_customers_title']}")
    shop_customers = ledger.customers(current_username)
    if shop_customers:
        for c in shop_customers:
            st.sidebar.markdown(f"• **{c}**")
    else:
        st.sidebar.caption(f"_{T['no_customers']}_")

    st.sidebar.markdown("---")
    st.sidebar.subheader(f"{T['quick_demo']}")
    st.sidebar.caption("Click any sample to test the NLP pipeline instantly:")

    # Tailor sample names to this shop if customers exist, or provide fresh names
    primary_cust = shop_customers[0] if shop_customers else ("రాము" if current_username == "chari" else "కస్టమర్")
    secondary_cust = shop_customers[1] if len(shop_customers) > 1 else ("సీతా" if current_username == "chari" else "రెండో_కస్టమర్")

    sample_phrases = [
        ("Telugu: Rice (బియ్యం / BM)", f"{primary_cust} 500 రూపాయలు బియ్యం"),
        ("Telugu: Sugar (పంచదార)", f"{secondary_cust} 200 రూపాయలు పంచదార"),
        ("Telugu: Oil (నూనె)", f"{primary_cust} 180 రూపాయలు నూనె"),
        ("Telugu: Ask Balance (బాకీ)", f"{primary_cust} ఎంత బాకీ"),
        ("Telugu: Payment (చెల్లింపు)", f"{primary_cust} 200 చెల్లించాడు"),
        ("Hindi: Flour (आटा)", f"{primary_cust} 300 रुपये आटा"),
        ("English: Correction", "make it 350"),
        ("English: Settle Full", f"{primary_cust} paid full"),
    ]

    for label, phrase in sample_phrases:
        if st.sidebar.button(label, key="btn_" + label):
            st.session_state["proposal"] = pipeline.understand(phrase, current_username)
            st.session_state["proposal"]["language"] = "te-IN / hi-IN / en-IN"
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Account: @{current_username} | Isolated Data Storage\nPowered by Gnani.ai Prisma v3.0")

    # --- MAIN DASHBOARD HEADER ---
    st.title(T["app_title"])
    st.markdown(f"### *{T['app_subtitle']}*")
    st.info(f"🏪 **{user.get('shop_name')}** (Owner: **{user.get('owner_name')}**) — Private Ledger Session")

    # --- METRIC CARDS ---
    metrics = ledger.financial_metrics(current_username)
    balances = ledger.all_balances(current_username)
    active_customers = len([b for b in balances.values() if b > 0])
    settled_customers = len([b for b in balances.values() if b == 0])
    total_entries_count = len(ledger.load_entries(current_username))

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric(T["outstanding"], f"₹{metrics['current_outstanding']:,.0f}")
    col_m2.metric(T["active_cust"], f"{active_customers}")
    col_m3.metric(T["settled_cust"], f"{settled_customers}")
    col_m4.metric(T["recovery_rate"], f"{metrics['recovery_rate']}%")
    col_m5.metric(T["total_entries"], f"{total_entries_count}")

    # --- SOUNDBOX NOTIFICATION BANNER ---
    message = st.session_state.pop("message", None)
    if message:
        if message["ok"]:
            st.success(f"🎉 {message['message']}")
            if message.get("soundbox_text"):
                components.html(tts.soundbox_html(message["soundbox_text"], current_lang), height=85)
        else:
            st.error(f"❌ {message['message']}")

    st.markdown("---")

    # =====================================================================
    # SECTION 1 & 2: VOICE INPUT & PROPOSAL
    # =====================================================================
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader(T["step1_title"])
        audio = st.audio_input(T["record_hint"])
        uploaded = st.file_uploader(T["or_upload"], type=["wav", "mp3", "m4a", "ogg", "flac", "aac"])
        clip = audio if audio is not None else uploaded
        if clip is not None:
            st.audio(clip)
            if st.button(T["btn_transcribe"], type="primary"):
                ext = os.path.splitext(getattr(clip, "name", "x.wav"))[1] or ".wav"
                path = "temp_clip" + ext
                with open(path, "wb") as f:
                    f.write(clip.getvalue())
                try:
                    with st.spinner("Listening via Gnani Prisma v3.0..."):
                        st.session_state["proposal"] = pipeline.propose(path, current_username)
                except Exception as e:
                    st.error(f"Error: {e}")
                if os.path.exists(path):
                    os.remove(path)
                st.rerun()

    with col_right:
        st.subheader(T["step2_title"])
        proposal = st.session_state.get("proposal")

        if proposal:
            st.info(f"**{T['heard']}** \"{proposal['transcript']}\"")
            st.markdown(f"**{T['intent']}** `{proposal['intent'].upper()}` | **{T['lang']}** `{proposal.get('language', 'Auto')}`")

            # Show issues if any
            if proposal["problems"]:
                st.warning("⚠️ Action required: " + ", ".join(proposal["problems"]))

                # Fallback if only customer name is missing
                if proposal["problems"] == ["customer name not found"]:
                    typed = st.text_input("Type customer name to continue:")
                    if st.button("Save with this name") and typed.strip():
                        proposal["entry"]["customer"] = typed.strip()
                        proposal["problems"] = []
                        st.session_state["message"] = pipeline.confirm(proposal, current_username, lang=current_lang)
                        st.session_state.pop("proposal")
                        st.rerun()
            else:
                entry = proposal["entry"]
                name_choice = entry.get("customer") or ""
                item_val = entry.get("item") or "—"
                amount_val = entry.get("amount") or "—"

                st.markdown(f"**{T['customer']}** `{name_choice}` | **{T['amount']}** `₹{amount_val}` | **{T['provision']}** `{item_val}`")

                if proposal["intent"] != "correct":
                    similar = proposal.get("similar_to")
                    if similar:
                        st.warning(f"Heard '{entry['customer']}'. Did you mean saved customer '{similar}'?")
                        options = [similar, entry["customer"]] if proposal["intent"] == "pay" else [entry["customer"], similar]
                        name_choice = st.radio("Select Customer:", options)
                    else:
                        name_choice = st.text_input(f"{T['customer']} (edit if needed):", value=entry["customer"])

                c_btn1, c_btn2 = st.columns(2)
                if c_btn1.button(T["btn_confirm"], type="primary"):
                    if proposal["intent"] != "correct" and name_choice.strip():
                        entry["customer"] = name_choice.strip()
                    st.session_state["message"] = pipeline.confirm(proposal, current_username, lang=current_lang)
                    st.session_state.pop("proposal")
                    st.rerun()

                if c_btn2.button(T["btn_cancel"]):
                    st.session_state.pop("proposal")
                    st.rerun()
        else:
            st.caption("Record voice or click a quick demo button on the sidebar to preview understanding.")

    st.markdown("---")

    # =====================================================================
    # SECTION 3: THE KHATA LEDGER (Tabs)
    # =====================================================================
    st.subheader(T["step3_title"])

    summary = ledger.customers_summary(current_username)
    all_entries = ledger.load_entries(current_username)

    tab_balances, tab_history, tab_manual, tab_analytics = st.tabs([
        T["tab_balances"],
        T["tab_history"],
        T["tab_manual"],
        T["tab_analytics"],
    ])

    # ----------------------------------------------------------------
    # TAB 1: BALANCES & CUSTOMER DRILL-DOWN
    # ----------------------------------------------------------------
    with tab_balances:
        if summary:
            # Quick Balance Lookup
            st.markdown(f"#### {T['quick_lookup']}")
            lookup_col1, lookup_col2 = st.columns([2, 1])
            with lookup_col1:
                lookup_name = st.selectbox(
                    "Select customer for instant balance:",
                    options=["— Select —"] + [s["Customer"] for s in summary],
                    key="quick_lookup_select",
                    label_visibility="collapsed"
                )
            with lookup_col2:
                if lookup_name and lookup_name != "— Select —":
                    bal = ledger.balance(lookup_name, current_username)
                    prov = ledger.customer_provisions(lookup_name, current_username)
                    if bal > 0:
                        st.error(f"**{lookup_name}** బాకీ: **₹{bal:,}** | {prov}")
                    elif bal == 0:
                        st.success(f"**{lookup_name}** — ✅ క్లియర్ (Settled)")
                    else:
                        st.info(f"**{lookup_name}** — 💚 అడ్వాన్స్: ₹{abs(bal):,}")

            st.markdown("---")

            # Search Filter
            search_query = st.text_input(T["search_label"], placeholder="Search by name or provision...").strip().lower()

            filtered_summary = summary
            if search_query:
                filtered_summary = [s for s in summary if search_query in s["Customer"].lower() or search_query in s["Provisions"].lower()]

            df_summary = pd.DataFrame(filtered_summary)
            if not df_summary.empty:
                # Localize status strings
                def map_status(val):
                    if "Settled" in val or "క్లియర్" in val:
                        return T["status_settled"]
                    elif "Owes" in val or "బాకీ" in val:
                        return T["status_owes"]
                    return T["status_advance"]

                df_summary["Status"] = df_summary["Status"].apply(map_status)

                df_display = df_summary.rename(columns={
                    "Customer": T["col_customer"],
                    "Balance": T["col_balance"],
                    "Provisions": T["col_provisions"],
                    "Status": T["col_status"]
                })
                st.dataframe(df_display, use_container_width=True)

                # --- CUSTOMER DRILL-DOWN ---
                st.markdown(f"#### {T['customer_detail']}")
                detail_customer = st.selectbox(
                    "Select a customer to view full transaction history:",
                    options=["— Select —"] + [s["Customer"] for s in summary],
                    key="detail_customer_select"
                )
                if detail_customer and detail_customer != "— Select —":
                    cust_hist = ledger.customer_history(detail_customer, current_username)
                    if cust_hist:
                        df_hist = pd.DataFrame(cust_hist)
                        # Style the dataframe for readability
                        display_cols = ["date", "item", "amount", "type", "running_balance"]
                        df_hist_display = df_hist[[c for c in display_cols if c in df_hist.columns]]
                        df_hist_display = df_hist_display.rename(columns={
                            "date": "Date", "item": "Provision/Item",
                            "amount": "Amount (₹)", "type": "Type",
                            "running_balance": "Running Balance (₹)"
                        })
                        st.dataframe(df_hist_display, use_container_width=True)
                        # Balance summary for this customer
                        final_bal = cust_hist[-1]["running_balance"] if cust_hist else 0
                        if final_bal > 0:
                            st.warning(f"📌 **{detail_customer}** total outstanding: **₹{final_bal:,}**")
                        elif final_bal == 0:
                            st.success(f"✅ **{detail_customer}** — All dues cleared!")
                        else:
                            st.info(f"💚 **{detail_customer}** has an advance of ₹{abs(final_bal):,}")
                    else:
                        st.info("No entries found for this customer.")

                # --- 1-Click WhatsApp Reminder ---
                st.markdown("#### " + T["send_whatsapp"])
                debtors = [s for s in summary if s["Balance"] > 0]
                if debtors:
                    wa_col1, wa_col2 = st.columns([1, 1.5])
                    with wa_col1:
                        target_cust = st.selectbox("Select Customer to Send Reminder:", options=[d["Customer"] for d in debtors])
                    with wa_col2:
                        cust_data = next((d for d in debtors if d["Customer"] == target_cust), None)
                        if cust_data:
                            wa_url = tts.generate_whatsapp_link(
                                cust_data["Customer"],
                                cust_data["Balance"],
                                cust_data["Provisions"],
                                shop_name=user.get("shop_name", "కిరాణా షాపు"),
                                lang=current_lang
                            )
                            st.markdown(f"""
                            <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                                <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:8px; font-weight:bold; cursor:pointer; margin-top:24px; display:flex; align-items:center; gap:8px;">
                                    <span>💬</span> Send WhatsApp Reminder to {target_cust} (₹{cust_data['Balance']})
                                </button>
                            </a>
                            """, unsafe_allow_html=True)
                else:
                    st.success("🎉 No outstanding dues! All customers are settled.")
            else:
                st.info("No matching records found for your search query.")
        else:
            st.info(T["empty_ledger"])

    # ----------------------------------------------------------------
    # TAB 2: FULL HISTORY WITH DATE FILTER & UNDO
    # ----------------------------------------------------------------
    with tab_history:
        if all_entries:
            df_entries = pd.DataFrame(all_entries)

            # Date Range Filter
            st.markdown("#### 📅 Filter by Date Range")
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                # Find min/max dates from entries
                try:
                    all_dates = [datetime.strptime(e.get("date", str(date.today())), "%Y-%m-%d").date() for e in all_entries]
                    min_date = min(all_dates)
                    max_date = max(all_dates)
                except Exception:
                    min_date = date.today()
                    max_date = date.today()
                filter_start = st.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date, key="hist_start")
            with date_col2:
                filter_end = st.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date, key="hist_end")

            # Apply date filter
            if "date" in df_entries.columns:
                df_entries["date"] = pd.to_datetime(df_entries["date"], errors="coerce").dt.date
                df_filtered = df_entries[
                    (df_entries["date"] >= filter_start) & (df_entries["date"] <= filter_end)
                ]
            else:
                df_filtered = df_entries

            # Customer filter
            hist_cust_filter = st.selectbox(
                "Filter by Customer (optional):",
                options=["All Customers"] + sorted(df_entries["customer"].dropna().unique().tolist()),
                key="hist_cust_filter"
            )
            if hist_cust_filter != "All Customers" and "customer" in df_filtered.columns:
                df_filtered = df_filtered[df_filtered["customer"] == hist_cust_filter]

            st.dataframe(df_filtered, use_container_width=True)
            st.caption(f"Showing {len(df_filtered)} of {len(df_entries)} entries")

            # Export option
            csv_data = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button(T["btn_export"], data=csv_data, file_name=f"khata_{current_username}.csv", mime="text/csv")

            st.markdown("---")

            # --- UNDO LAST ENTRY ---
            st.markdown(f"#### {T['undo_last']}")
            if all_entries:
                last_e = all_entries[-1]
                st.warning(
                    f"Last entry: **{last_e.get('customer')}** | "
                    f"₹{last_e.get('amount')} | "
                    f"{last_e.get('item', '—')} | "
                    f"Date: {last_e.get('date', '—')}"
                )
                undo_col1, undo_col2 = st.columns([1, 3])
                with undo_col1:
                    if st.button("🗑️ Undo / Delete This Entry", type="secondary", key="undo_btn"):
                        st.session_state["confirm_undo"] = True

                if st.session_state.get("confirm_undo"):
                    st.error("⚠️ Are you sure? This will permanently remove the last entry.")
                    yes_col, no_col = st.columns(2)
                    if yes_col.button("✅ Yes, Delete It", key="undo_yes"):
                        deleted = ledger.delete_last_entry(current_username)
                        st.session_state["confirm_undo"] = False
                        if deleted:
                            st.success(f"✅ Deleted: {deleted.get('customer')} ₹{deleted.get('amount')}")
                        st.rerun()
                    if no_col.button("❌ No, Keep It", key="undo_no"):
                        st.session_state["confirm_undo"] = False
                        st.rerun()
        else:
            st.info(T["empty_ledger"])

    # ----------------------------------------------------------------
    # TAB 3: MANUAL ENTRY (No Mic / No API Key needed)
    # ----------------------------------------------------------------
    with tab_manual:
        st.markdown(f"#### {T['manual_entry_title']}")
        st.caption("Works fully offline — no microphone or API key required. Perfect for quick entries via keyboard.")

        m_col1, m_col2 = st.columns(2)

        with m_col1:
            st.markdown("##### ➕ Add Credit Entry")
            # Customer name: type new or pick existing
            existing_customers = ledger.customers(current_username)
            manual_name_mode = st.radio(
                "Customer Name:",
                options=["Type new name", "Pick existing customer"],
                key="manual_name_mode",
                horizontal=True
            )
            if manual_name_mode == "Pick existing customer" and existing_customers:
                manual_customer = st.selectbox("Customer:", existing_customers, key="manual_cust_select")
            else:
                manual_customer = st.text_input(T["manual_name"], placeholder="e.g. రాము / Ramu", key="manual_cust_new")

            manual_amount = st.number_input(T["manual_amount"], min_value=1, max_value=100000, value=100, step=10, key="manual_amt")

            manual_provision_sel = st.selectbox(T["manual_provision"], options=PROVISION_LIST, key="manual_prov_sel")
            if manual_provision_sel == "Other":
                manual_provision = st.text_input("Enter custom provision name:", key="manual_prov_custom")
            elif manual_provision_sel.startswith("—"):
                manual_provision = None
            else:
                manual_provision = manual_provision_sel

            if st.button(T["manual_btn_add"], type="primary", key="manual_add_btn"):
                if not manual_customer or not manual_customer.strip():
                    st.error("Please enter customer name.")
                else:
                    saved = ledger.add_entry({
                        "customer": manual_customer.strip(),
                        "amount": int(manual_amount),
                        "item": manual_provision or "—",
                        "type": "credit"
                    }, current_username)
                    sb = tts.format_announcement("add", saved["customer"], saved["amount"], provision=saved.get("item"), lang=current_lang)
                    st.session_state["message"] = {"ok": True, "message": f"Added: {saved['customer']} ₹{saved['amount']}", "soundbox_text": sb}
                    st.rerun()

        with m_col2:
            st.markdown("##### 💳 Record Payment")
            existing_debtors = [s["Customer"] for s in (ledger.customers_summary(current_username) or []) if s["Balance"] > 0]
            if existing_debtors:
                pay_customer = st.selectbox("Customer with Outstanding:", existing_debtors, key="pay_cust_select")
                current_bal = ledger.balance(pay_customer, current_username)
                st.info(f"Current balance for **{pay_customer}**: ₹{current_bal:,}")

                pay_mode = st.radio(
                    "Payment Amount:",
                    options=["Partial Amount", "Pay Full Balance"],
                    key="pay_mode",
                    horizontal=True
                )
                if pay_mode == "Pay Full Balance":
                    pay_amount = current_bal
                    st.markdown(f"💰 Full payment: **₹{pay_amount:,}**")
                else:
                    pay_amount = st.number_input("Payment Amount (₹):", min_value=1, max_value=int(current_bal), value=min(100, int(current_bal)), step=10, key="pay_amt_input")

                if st.button(T["manual_btn_pay"], type="primary", key="manual_pay_btn"):
                    ledger.add_payment(pay_customer, pay_amount, current_username)
                    remaining = current_bal - pay_amount
                    sb = tts.format_announcement("pay", pay_customer, pay_amount, remaining=remaining, lang=current_lang)
                    tail = "Fully Settled!" if remaining == 0 else f"Balance: ₹{remaining:,}"
                    st.session_state["message"] = {"ok": True, "message": f"{pay_customer} paid ₹{pay_amount}. {tail}", "soundbox_text": sb}
                    st.rerun()
            else:
                st.info("No customers with outstanding balance found. Add credit entries first.")

    # ----------------------------------------------------------------
    # TAB 4: ANALYTICS (Enhanced)
    # ----------------------------------------------------------------
    with tab_analytics:
        st.markdown("### 📊 " + T["tab_analytics"])
        st.caption("Visual business insights computed in real-time from your voice ledger entries.")

        # Row 1: Top Debtors + Top Provisions
        c_an1, c_an2 = st.columns(2)

        with c_an1:
            st.markdown(f"#### {T['top_debtors_title']}")
            debtors_data = {s["Customer"]: s["Balance"] for s in summary if s["Balance"] > 0}
            if debtors_data:
                df_chart = pd.DataFrame(list(debtors_data.items()), columns=["Customer", "Outstanding (₹)"]).set_index("Customer")
                st.bar_chart(df_chart)
            else:
                st.success("🎉 All accounts are settled! Zero outstanding debt.")

        with c_an2:
            st.markdown(f"#### {T['top_provisions_title']}")
            prov_data = ledger.provisions_stats(current_username)
            if prov_data:
                df_prov = pd.DataFrame(list(prov_data.items()), columns=["Provision", "Orders"]).set_index("Provision")
                st.bar_chart(df_prov)
            else:
                st.info("No provision entries recorded yet.")

        st.markdown("---")

        # Row 2: Financial Summary Cards
        st.markdown("#### 💰 Financial Summary")
        fs_col1, fs_col2, fs_col3 = st.columns(3)
        fs_col1.metric(T["total_credit"], f"₹{metrics['total_credit']:,.0f}")
        fs_col2.metric(T["total_collected"], f"₹{metrics['total_collected']:,.0f}")
        fs_col3.metric(T["recovery_rate"], f"{metrics['recovery_rate']}%",
                       delta=f"{'On Track' if metrics['recovery_rate'] >= 50 else 'Needs Attention'}")

        st.markdown("---")

        # Row 3: Monthly Trend Chart
        st.markdown(f"#### {T['trend_title']}")
        monthly_data = ledger.monthly_summary(current_username)
        if monthly_data:
            df_monthly = pd.DataFrame([
                {"Month": k, "Credit Given (₹)": v["credit"], "Payment Received (₹)": v["payment"]}
                for k, v in monthly_data.items()
            ]).set_index("Month")
            st.line_chart(df_monthly)
            st.caption("📌 Blue = Credit given to customers | Orange = Payments received from customers")
        else:
            st.info("Add more entries over multiple days to see the monthly trend chart.")

        st.markdown("---")

        # Row 4: Customer Comparison Table
        if summary:
            st.markdown("#### 📋 All Customers — Balance Summary")
            df_full = pd.DataFrame(summary)
            df_full["Balance"] = df_full["Balance"].apply(lambda x: f"₹{x:,}")
            st.dataframe(df_full.rename(columns={
                "Customer": T["col_customer"],
                "Balance": T["col_balance"],
                "Provisions": T["col_provisions"],
                "Status": T["col_status"]
            }), use_container_width=True)
