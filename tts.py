import urllib.parse


def format_announcement(intent, customer, amount=None, remaining=None, provision=None, lang="te"):
    """
    Generates natural, soundbox-style announcements for retail store transactions.
    """
    amt_str = str(abs(amount)) if amount is not None else ""
    rem_str = str(remaining) if remaining is not None else ""
    cust_str = customer or "కస్టమర్"

    if lang == "te":
        if intent == "add":
            prov_txt = f" ({provision})" if provision and provision != "—" else ""
            return f"{cust_str} ఖాతాలో {amt_str} రూపాయలు నమోదయ్యాయి{prov_txt}."
        elif intent == "pay":
            tail = "ఖాతా పూర్తిగా క్లియర్ అయ్యింది." if remaining == 0 else f"మిగిలిన బాకీ {rem_str} రూపాయలు."
            return f"{cust_str} {amt_str} రూపాయలు చెల్లించారు. {tail}"
        elif intent == "ask":
            return f"{cust_str} బాకీ మొత్తం {rem_str} రూపాయలు."
        elif intent == "correct":
            return f"చివరి ఎంట్రీ మొత్తం {amt_str} రూపాయలుగా సవరించబడింది."
        return "లావాదేవీ పూర్తయ్యింది."

    elif lang == "hi":
        if intent == "add":
            prov_txt = f" ({provision})" if provision and provision != "—" else ""
            return f"{cust_str} के खाते में {amt_str} रुपये दर्ज हुए{prov_txt}."
        elif intent == "pay":
            tail = "खाता पूरी तरह चुकता हो गया." if remaining == 0 else f"बाकी बचे {rem_str} रुपये."
            return f"{cust_str} ने {amt_str} रुपये चुकाए. {tail}"
        elif intent == "ask":
            return f"{cust_str} का कुल बाकी {rem_str} रुपये है."
        elif intent == "correct":
            return f"अंतिम एंट्री {amt_str} रुपये पर संशोधित की गई."
        return "लेन-देन दर्ज हुआ."

    else:  # en
        if intent == "add":
            prov_txt = f" for {provision}" if provision and provision != "—" else ""
            return f"{amt_str} rupees added to {cust_str}'s account{prov_txt}."
        elif intent == "pay":
            tail = "Account is fully settled." if remaining == 0 else f"Balance now {rem_str} rupees."
            return f"{cust_str} paid {amt_str} rupees. {tail}"
        elif intent == "ask":
            return f"{cust_str} owes {rem_str} rupees."
        elif intent == "correct":
            return f"Last entry corrected to {amt_str} rupees."
        return "Transaction recorded successfully."


def soundbox_html(text, lang="te"):
    """
    Renders an interactive, auto-playing Soundbox announcement widget with Web Speech API.
    """
    lang_code = "te-IN" if lang == "te" else ("hi-IN" if lang == "hi" else "en-IN")
    escaped_text = text.replace('"', '\\"').replace("'", "\\'")

    return f"""
    <div style="background: linear-gradient(135deg, #1A365D, #2B6CB0); color: white; padding: 14px 20px; border-radius: 12px; margin: 12px 0 16px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: space-between; font-family: sans-serif;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(255,255,255,0.2); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px;">
                🔊
            </div>
            <div>
                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #CBD5E0; font-weight: 600;">
                    Khata Voice Smart Soundbox
                </div>
                <div style="font-size: 15px; font-weight: 500; margin-top: 2px;">
                    "{text}"
                </div>
            </div>
        </div>
        <button onclick="speakSoundbox()" style="background: #ECC94B; color: #1A202C; border: none; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: bold; cursor: pointer; transition: 0.2s; display: flex; align-items: center; gap: 6px;">
            <span>▶</span> Replay Audio
        </button>
    </div>
    <script>
    function speakSoundbox() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance("{escaped_text}");
            utterance.lang = "{lang_code}";
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
        }}
    }}
    // Auto-announce on render
    setTimeout(speakSoundbox, 400);
    </script>
    """


def generate_whatsapp_link(customer_name, balance, provisions, shop_name="శ్రీ లక్ష్మి కిరాణా", lang="te"):
    """
    Generates a pre-filled WhatsApp payment reminder link with exact balance and provisions.
    """
    if lang == "te":
        msg = f"నమస్కారం {customer_name} గారు, మీ {shop_name} దుకాణం బాకీ మొత్తం ₹{balance:,} (సరుకులు: {provisions}). దయచేసి వీలైనంత త్వరగా చెల్లించగలరు. ధన్యవాదాలు!"
    elif lang == "hi":
        msg = f"नमस्ते {customer_name} जी, आपकी {shop_name} की कुल बाकी राशि ₹{balance:,} है (सामान: {provisions}). कृपया जल्द से जल्द भुगतान करें. धन्यवाद!"
    else:
        msg = f"Hello {customer_name}, your outstanding balance at {shop_name} is ₹{balance:,} (Provisions: {provisions}). Kindly clear the dues at your earliest convenience. Thank you!"

    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/?text={encoded_msg}"


if __name__ == "__main__":
    t_msg = format_announcement("add", "రాము", 500, provision="బియ్యం (Rice)", lang="te")
    print("Telugu Add:", t_msg)
    p_msg = format_announcement("pay", "రాము", 200, remaining=300, lang="te")
    print("Telugu Pay:", p_msg)
    wa_url = generate_whatsapp_link("రాము", 400, "బియ్యం, పంచదార")
    print("WhatsApp Link:", wa_url)
