import requests, base64

API_BASE_URL = f"https://api16-normal-v6.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"

url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
payload = {"text": "A hiccup is an involuntary contraction of the diaphragm that may repeat several times per minute. Once triggered, the reflex causes a strong contraction of the diaphragm followed about a quarter of a second later by closure of the epiglottis which results in the 'hic' sound. ", "voice": "en_us_rocket"}
r = requests.post(url, json=payload)

audio = r.json()
audio_bytes = base64.b64decode(audio["data"])
with open("output.mp3", "wb") as f:
    f.write(audio_bytes)

# en_us_001 = tiktok lady
# en_us_002 = tiktok lady
# en_us_006 = tiktok man
# en_us_007 = tiktok man
# en_uk_001 = english man
# en_uk_003 = english man DEEP
# en_us_008 = arrested development narrator
# en_us_009 = arrested development narrator
# en_us_010 = tiktok man low
#en_us_rocket = rocket raccoon

