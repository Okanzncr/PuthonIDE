import urllib.request
import json
import sys

GROQ_API_KEY = "BURAYA_KENDI_GROQ_API_ANAHTAR
INIZI_YAPISTIRIN"
GROQ_MODEL = "llama-3.1-8b-instant"

RENK_YESIL = "\033[92m"
RENK_MAVI = "\033[94m"
RENK_SIYAH = "\033[0m"
RENK_SARI = "\033[93m"
RENK_KIRMIZI = "\033[91m"
RENK_BEYAZ = "\033[97m"

SISTEM_TALIMATI = """
Sen derin, ozgur ve analitik dusunen bir
yapay zeka asistanisin.
Kullanici '/github kullanici/repo' yazarsa o
projeyi,
'/profil kullanici_adi' yazarsa o kisinin
profilini hafizana alirsin.
Cevaplarin kisa ve mobil ekrana uygun olsun.
"""

sohbet_gecmisi = [{"role": "system",
"content": SISTEM_TALIMATI}]
hafiza = {"github": {}, "profil": {}}

def ekrani_temizle():
    print("\033c", end="")

def github_api_get(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "PythonIDE-App")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"hata": str(e)}

def groq_chat(messages):
    if "BURAYA" in GROQ_API_KEY:
        return "HATA: Lutfen egeny.py icindeki GROQ_API_KEY kismina kendi anahtarinizi yazin."
    url = "https://api.groq.com/openai/v1/chat/completions"
    data = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={
            "Authorization": "Bearer " + GROQ_API_KEY,
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return "API Hatasi: " + str(e)

def komut_isle(komut):
    parcalar = komut.split()
    if len(parcalar) < 2:
        return None
    if parcalar[0] == "/github" and len(parcalar) >= 3:
        kullanici = parcalar[1]
        repo = parcalar[2]
        url = "https://api.github.com/repos/" + kullanici + "/" + repo
        veri = github_api_get(url)
        if "hata" not in veri:
            hafiza["github"][kullanici + "/" + repo] = veri
            return RENK_YESIL + "OK: " + kullanici + "/" + repo + " hafizaya alindi." + RENK_SIYAH + "\nAciklama: " + str(veri.get("description", "Yok")) + "\nYildiz: " + str(veri.get("stargazers_count", 0))
        else:
            return RENK_KIRMIZI + "Hata: " + veri["hata"] + RENK_SIYAH
    elif parcalar[0] == "/profil" and len(parcalar) >= 2:
        kullanici = parcalar[1]
        url = "https://api.github.com/users/" + kullanici
        veri = github_api_get(url)
        if "hata" not in veri:
            hafiza["profil"][kullanici] = veri
            repo_url = "https://api.github.com/users/" + kullanici + "/repos?per_page=10"
            repolar = github_api_get(repo_url)
            liste = ""
            if isinstance(repolar, list):
                for r in repolar[:5]:
                    liste += "- " + r["name"] + ": " + str(r.get("description", ""))[:40] + "\n"
            return RENK_YESIL + "OK: " + kullanici + " profili alindi." + RENK_SIYAH + "\nAd: " + str(veri.get("name", "Yok")) + "\nRepolar:\n" + liste
        else:
            return RENK_KIRMIZI + "Hata: " + veri["hata"] + RENK_SIYAH
    return None

def arayuzu_baslat():
    ekrani_temizle()
    print(RENK_MAVI + "=== PuthonIDE ===" + RENK_SIYAH)
    print(RENK_SARI + "Komutlar: /github k/repo | /profil k | cikis" + RENK_SIYAH)
    print()
    while True:
        try:
            girdi = input(RENK_YESIL + "Sen: " + RENK_SIYAH).strip()
            if not girdi:
                continue
            if girdi.lower() in ["cikis", "exit", "quit"]:
                print("Gorusmek uzere!")
                break
            if girdi.startswith("/"):
                sonuc = komut_isle(girdi)
                if sonuc:
                    print(sonuc)
                    continue
            sohbet_gecmisi.append({"role": "user", "content": girdi})
            print(RENK_MAVI + "Dusunuyor..." + RENK_SIYAH)
            cevap = groq_chat(sohbet_gecmisi)
            print(RENK_BEYAZ + "Asistan: " + cevap + RENK_SIYAH + "\n")
            sohbet_gecmisi.append({"role": "assistant", "content": cevap})
            if len(sohbet_gecmisi) > 21:
                sohbet_gecmisi = [sohbet_gecmisi[0]] + sohbet_gecmisi[-20:]
        except KeyboardInterrupt:
            print("\nCikis yapiliyor...")
            break
        except Exception as e:
            print(RENK_KIRMIZI + "Hata: " + str(e) + RENK_SIYAH)

if __name__ == "__main__":
    arayuzu_baslat()
