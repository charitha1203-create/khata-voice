import re
import difflib

FILLER = ["credit", "rupees", "rupee", "rs", "took", "taken", "for", "to", "of", "the", "and",
	"paid", "pay", "payment", "gave", "returned", "cleared", "settled", "back", "full", "fully", "all", "everything",
	"రూపాయలు", "రూపాయల", "రూపాయ", "కి", "కు",
	"చెల్లించాడు", "చెల్లించారు", "చెల్లింపు", "కట్టాడు", "కట్టారు",
	"रुपये", "रुपए", "रुपया", "का", "की", "के", "को", "ने",
	"चुकाया", "चुकाए", "भुगतान", "वापस", "जमा"]
PUNCT = ".,!?:;₹।"

ITEM_ALIASES = {
	"bm": "బియ్యం (Rice)",
	"biyyam": "బియ్యం",
	"rice": "బియ్యం (Rice)",
	"panchadar": "పంచదార",
	"panchadara": "పంచదార",
	"sugar": "పంచదార (Sugar)",
	"pappu": "కందిపప్పు",
	"kandi pappu": "కందిపప్పు",
	"dal": "పప్పు (Dal)",
	"nune": "నూనె",
	"oil": "నూనె (Oil)",
	"sabbu": "సబ్బు",
	"soap": "సబ్బు (Soap)",
	"aata": "గోధుమ పిండి (Aata)",
	"pindi": "పిండి",
	"tea": "టీ పొడి (Tea)",
	"tea podi": "టీ పొడి",
}


def words_of(chunk):
	return [w.strip(PUNCT) for w in chunk.split() if w.strip(PUNCT)]


def find_amount(text):
	match = re.search(r"\d[\d,]*", text)
	if match:
		return int(match.group().replace(",", ""))
	return None


def find_customer(text, known):
	tokens = [w.lower() for w in words_of(text)]
	for name in sorted(known, key=lambda n: len(words_of(n)), reverse=True):
		parts = [p.lower() for p in words_of(name)]
		for i in range(len(tokens) - len(parts) + 1):
			if tokens[i:i + len(parts)] == parts:
				return name, None
	match = re.search(r"\d[\d,]*", text)
	before = text[:match.start()] if match else ""
	words = [w for w in words_of(before) if w.lower() not in FILLER]
	if not words:
		return None, None
	name = " ".join(words)
	name = name.title() if name.isascii() else name
	known_lower = {k.lower(): k for k in known}
	close = difflib.get_close_matches(name.lower(), list(known_lower), n=1, cutoff=0.75)
	return name, (known_lower[close[0]] if close else None)


def find_item(text, customer):
	match = re.search(r"\d[\d,]*", text)
	if not match:
		return None
	skip = set(w.lower() for w in (customer or "").split())
	items = [w for w in words_of(text[match.end():]) if w.lower() not in FILLER and w.lower() not in skip]
	if not items:
		return None
	raw_item = " ".join(items)
	lowered = raw_item.lower()
	if lowered in ITEM_ALIASES:
		return ITEM_ALIASES[lowered]
	return raw_item


def extract_entry(text, known=None):
	known = known or []
	customer, similar = find_customer(text, known)
	return {
		"customer": customer,
		"amount": find_amount(text),
		"item": find_item(text, customer),
		"similar_to": similar,
	}


if __name__ == "__main__":
	known = ["Ramu", "సీతా"]
	samples = [
		"Ramu 500 credit rice",
		"Sravya 300 rupees sugar",
		"సీమా 300 రూపాయలు బియ్యం",
		"రాము 500 bm",
		"రాము 200 panchadar",
		"రాము 150 nune",
		"रामू 300 रुपये आटा",
		"how much does Ramu owe",
	]
	for s in samples:
		print(s, "->", extract_entry(s, known))
