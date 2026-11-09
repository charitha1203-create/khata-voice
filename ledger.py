import json
import os
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_ledger_file(username=None):
	if not username:
		return os.path.join(BASE_DIR, "ledger.json")
	safe_name = "".join(c for c in username.strip().lower() if c.isalnum() or c in "_-")
	return os.path.join(BASE_DIR, f"ledger_{safe_name}.json")


def load_entries(username=None):
	filepath = get_ledger_file(username)
	if not os.path.exists(filepath):
		# Pre-populate demo records ONLY for chari demo account
		if username and username.strip().lower() == "chari":
			demo = [
				{"customer": "సీతా", "amount": 300, "item": "పంచదార", "type": "credit", "date": str(date.today())},
				{"customer": "సమంత", "amount": 300, "item": "బియ్యం", "type": "credit", "date": str(date.today())}
			]
			save_entries(demo, username)
			return demo
		# Any other new account gets an empty ledger
		save_entries([], username)
		return []
	try:
		with open(filepath, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return []


def save_entries(entries, username=None):
	filepath = get_ledger_file(username)
	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(entries, f, ensure_ascii=False, indent=2)


def add_entry(entry, username=None):
	entries = load_entries(username)
	new_entry = dict(entry)
	new_entry.setdefault("type", "credit")
	new_entry["date"] = str(date.today())
	entries.append(new_entry)
	save_entries(entries, username)
	return new_entry


def add_payment(customer, amount, username=None):
	return add_entry({"customer": customer, "amount": -abs(amount), "item": "payment", "type": "payment"}, username)


def balance(customer, username=None):
	return sum(e["amount"] for e in load_entries(username) if e.get("customer") == customer and e.get("amount") is not None)


def all_balances(username=None):
	totals = {}
	for e in load_entries(username):
		if e.get("customer") and e.get("amount") is not None:
			totals[e["customer"]] = totals.get(e["customer"], 0) + e["amount"]
	return totals


def customer_provisions(customer, username=None):
	entries = load_entries(username)
	items = []
	for e in entries:
		if e.get("customer") == customer and e.get("item") and e.get("item") != "payment":
			if e["item"] not in items:
				items.append(e["item"])
	return ", ".join(items) if items else "—"


def customer_history(customer, username=None):
	"""Return all ledger entries for a specific customer, with running balance column."""
	entries = load_entries(username)
	history = []
	running = 0
	for e in entries:
		if e.get("customer") == customer:
			running += e.get("amount", 0)
			row = dict(e)
			row["running_balance"] = running
			history.append(row)
	return history


def delete_last_entry(username=None):
	"""Remove the most recent entry from the ledger. Returns the deleted entry or None."""
	entries = load_entries(username)
	if not entries:
		return None
	deleted = entries.pop()
	save_entries(entries, username)
	return deleted


def customers_summary(username=None):
	totals = all_balances(username)
	entries = load_entries(username)
	items_map = {}
	for e in entries:
		c = e.get("customer")
		it = e.get("item")
		if c and it and it != "payment":
			if c not in items_map:
				items_map[c] = []
			if it not in items_map[c]:
				items_map[c].append(it)
	summary = []
	for name, total in totals.items():
		provisions = ", ".join(items_map.get(name, [])) or "—"
		status = "Settled (క్లియర్)" if total == 0 else ("Owes (బాకీ)" if total > 0 else "Advance (అడ్వాన్స్)")
		summary.append({
			"Customer": name,
			"Balance": total,
			"Provisions": provisions,
			"Status": status
		})
	return summary


def customers(username=None):
	return sorted({e["customer"] for e in load_entries(username) if e.get("customer")})


def correct_last(new_amount, username=None):
	entries = load_entries(username)
	if not entries:
		return None
	last = entries[-1]
	sign = -1 if last.get("amount") and last["amount"] < 0 else 1
	last["amount"] = sign * abs(new_amount)
	save_entries(entries, username)
	return last


def monthly_summary(username=None):
	"""Returns dict of {YYYY-MM: {credit: X, payment: Y, net: Z}} for trend charts."""
	entries = load_entries(username)
	monthly = {}
	for e in entries:
		raw_date = e.get("date", str(date.today()))
		try:
			month_key = str(raw_date)[:7]  # "YYYY-MM"
		except Exception:
			month_key = str(date.today())[:7]
		if month_key not in monthly:
			monthly[month_key] = {"credit": 0, "payment": 0, "net": 0}
		amt = e.get("amount", 0) or 0
		if amt > 0:
			monthly[month_key]["credit"] += amt
		else:
			monthly[month_key]["payment"] += abs(amt)
		monthly[month_key]["net"] += amt
	return dict(sorted(monthly.items()))


# --- ADVANCED KIRANA ANALYTICS ---
def financial_metrics(username=None):
	entries = load_entries(username)
	total_credit = sum(e["amount"] for e in entries if e.get("amount") and e["amount"] > 0)
	total_collected = sum(abs(e["amount"]) for e in entries if e.get("amount") and e["amount"] < 0)
	current_outstanding = total_credit - total_collected
	recovery_rate = (total_collected / total_credit * 100) if total_credit > 0 else 100.0
	return {
		"total_credit": total_credit,
		"total_collected": total_collected,
		"current_outstanding": current_outstanding,
		"recovery_rate": round(recovery_rate, 1)
	}


def provisions_stats(username=None):
	entries = load_entries(username)
	counts = {}
	for e in entries:
		it = e.get("item")
		if it and it != "payment":
			counts[it] = counts.get(it, 0) + 1
	return counts


if __name__ == "__main__":
	print("Chari metrics:", financial_metrics("chari"))
	print("Chari provisions:", provisions_stats("chari"))
	print("Chari monthly:", monthly_summary("chari"))
