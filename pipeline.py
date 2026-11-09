import os
from stt import transcribe_audio
from intent import detect_intent, contains, FULL_WORDS
from extract import extract_entry
import ledger
import tts


def understand(text, username=None):
	intent = detect_intent(text)
	known = ledger.customers(username)
	entry = extract_entry(text, known)
	similar = entry.pop("similar_to", None)
	if intent == "correct":
		entry["customer"] = None
		entry["item"] = None
		similar = None
	if intent == "pay":
		entry["item"] = "payment"
		entry["pay_full"] = (not entry["amount"]) and contains(text, FULL_WORDS)
	problems = []
	if intent in ("add", "ask", "pay") and not entry["customer"]:
		problems.append("customer name not found")
	if intent in ("add", "correct") and not entry["amount"]:
		problems.append("amount not found")
	if intent == "pay":
		if not entry["amount"] and not entry["pay_full"]:
			problems.append("amount not found")
		if entry["customer"] and entry["customer"] not in known and not similar:
			problems.append("'" + entry["customer"] + "' is not in the khata yet")
	return {"transcript": text, "intent": intent, "entry": entry, "problems": problems, "similar_to": similar}


def propose(audio_path, username=None):
	known = ledger.customers(username)
	result = transcribe_audio(audio_path, keyterms=known or None)
	proposal = understand(result["transcript"], username)
	proposal["language"] = result.get("detected_language_code")
	return proposal


def confirm(proposal, username=None, lang="te"):
	if proposal["problems"]:
		return {"ok": False, "message": "Cannot save: " + ", ".join(proposal["problems"])}
	intent = proposal["intent"]
	entry = proposal["entry"]
	if intent == "add":
		saved = ledger.add_entry({"customer": entry["customer"], "amount": entry["amount"], "item": entry["item"]}, username)
		sb = tts.format_announcement("add", saved["customer"], saved["amount"], provision=saved.get("item"), lang=lang)
		return {"ok": True, "message": "Saved: " + saved["customer"] + " " + str(saved["amount"]), "soundbox_text": sb}
	if intent == "pay":
		customer = entry["customer"]
		known = ledger.customers(username)
		if customer not in known:
			return {"ok": False, "message": customer + " is not in the khata yet"}
		owed = ledger.balance(customer, username)
		if owed <= 0:
			return {"ok": False, "message": customer + " owes nothing"}
		amount = owed if entry.get("pay_full") else entry["amount"]
		if amount > owed:
			return {"ok": False, "message": "Payment " + str(amount) + " is more than the balance " + str(owed)}
		ledger.add_payment(customer, amount, username)
		left = owed - amount
		tail = "Settled." if left == 0 else "Balance now " + str(left)
		sb = tts.format_announcement("pay", customer, amount, remaining=left, lang=lang)
		return {"ok": True, "message": customer + " paid " + str(amount) + ". " + tail, "soundbox_text": sb}
	if intent == "correct":
		fixed = ledger.correct_last(entry["amount"], username)
		if fixed is None:
			return {"ok": False, "message": "Nothing to correct yet"}
		sb = tts.format_announcement("correct", None, abs(fixed["amount"]), lang=lang)
		return {"ok": True, "message": "Corrected last entry to " + str(abs(fixed["amount"])), "soundbox_text": sb}
	if intent == "ask":
		total = ledger.balance(entry["customer"], username)
		sb = tts.format_announcement("ask", entry["customer"], remaining=total, lang=lang)
		return {"ok": True, "message": entry["customer"] + " owes " + str(total), "soundbox_text": sb}
	return {"ok": False, "message": "Not understood"}


if __name__ == "__main__":
	test_u = "test_user_pipe"
	try:
		p = understand("Ramu 500 credit rice", test_u)
		res = confirm(p, test_u, lang="te")
		print("Confirm result:", res)
	finally:
		f = ledger.get_ledger_file(test_u)
		if os.path.exists(f):
			os.remove(f)
