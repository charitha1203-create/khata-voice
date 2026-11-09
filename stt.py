import requests, os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
	key = os.environ.get("GNANI_API_KEY")
	if not key:
		raise RuntimeError("GNANI_API_KEY is not set. Please set it in your environment or in a .env file.")
	return key

def transcribe_audio(audio_path, languages="te-IN,hi-IN,en-IN", keyterms=None):
	key = get_api_key()
	headers = {"X-API-Key-ID": key}
	data = {"model": "prisma-v3.0", "language_code": languages, "format": "transcribe"}
	if keyterms:
		data["keyterms"] = ",".join(keyterms)
	with open(audio_path, "rb") as f:
		response = requests.post("https://api.vachana.ai/stt/v3", headers=headers, files={"audio_file": f}, data=data, timeout=60)
	if response.status_code != 200:
		raise RuntimeError(f'STT failed: {response.status_code} {response.text}')
	return response.json()

if __name__ == "__main__":
	result = transcribe_audio("telugu1.m4a")
	print(result["transcript"])
	print(result.get("detected_language_code"))
