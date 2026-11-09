import re

ASK_WORDS = ["how much", "balance", "owes", "total", "कितना", "बाकी", "हिसाब", "ఎంత", "బాకీ", "మొత్తం"]
CORRECT_WORDS = ["make it", "change", "wrong", "correct", "mistake", "गलत", "बदल", "सुधार", "తప్పు", "మార్చు", "సరిచేయి"]
PAY_WORDS = ["paid", "pay", "payment", "cleared", "settled", "returned", "gave back",
	"चुका", "भुगतान", "वापस", "जमा",
	"చెల్లించ", "చెల్లింపు", "కట్టా", "తీర్చ"]
FULL_WORDS = ["full", "fully", "all", "everything", "whole", "balance",
	"पूरा", "पूरी", "सारा", "మొత్తం", "అంతా", "పూర్తి"]


def contains(text, words):
	lowered = text.lower()
	padded = " " + re.sub(r"[^\w\s]", " ", lowered) + " "
	for w in words:
		if w.isascii():
			if " " + w + " " in padded:
				return True
		elif w in lowered:
			return True
	return False


def detect_intent(text):
	if contains(text, CORRECT_WORDS):
		return "correct"
	if contains(text, PAY_WORDS):
		return "pay"
	if contains(text, ASK_WORDS):
		return "ask"
	return "add"


if __name__ == "__main__":
	samples = [
		"Ramu 500 credit rice",
		"how much does Ramu owe",
		"make it 600",
		"रामू का कितना बाकी है",
		"రాము ఎంత బాకీ",
		"Ramu paid 200",
		"Ramu paid full",
		"रामू ने 200 चुकाए",
		"రాము 200 చెల్లించాడు",
	]
	for s in samples:
		print(s, "->", detect_intent(s))
