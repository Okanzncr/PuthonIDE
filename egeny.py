import urllib.request
import json
import base64
import time

# ==========================================
# 1. AYARLAR VE API ANAHTARI
# ==========================================
# BURAYA KENDİ GROQ API ANAHTARINIZI YAPISTIRIN
GROQ_API_KEY = "BURAYA_KENDI_GROQ_API_ANAHTARINIZI_YAPISTIRIN"

# Renk Kodları (Terminalde renkli yazı için)
RENK_YESIL = "\033[92m"
RENK_MAVI = "\033[94m"
RENK_SIYAH = "\033[0m"
RENK_SARI = "\033[93m"
RENK_KIRMIZI = "\033[91m"

# Yapay Zekanın Kişiliği (System Prompt)
SISTEM_TALIMATI = """
Sen derin, özgür ve analitik düşünen bir yapay zeka asistanısın. 
Kullanıcı sana '/github kullanici/repo' komutu verirse o projeyi, '/profil kullanici_adi' komutu verirse o kişinin GitHub profilini ve repolarını hafızana alırsın. 
Sonraki soruları bu bilgileri kullanarak detaylıca cevaplarsın.
"""

# Sohbet hafızası (Geçmişi tutar)
sohbet_gecmisi = [{"role": "system", "content": SISTEM_TALIMATI}]
# ==========================================

def ekrani_temizle():
    # iOS uyumlu terminal temizleme
    print("\033c", end="")

def github_api_get(url):
    # GitHub API'sine GET isteği atan yardımcı fonksiyon
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "PythonIDE-App")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"{RENK_KIRMIZI}[API HATASI]: {e}{RENK_SIYAH}")
        return None

def github_profilini_hafizaya_al(kullanici_adi):
    # Kullanıcı profili ve repolarını çeken fonksiyon
    print(f"\n{RENK_SARI}[SİSTEM]: '{kullanici_adi}' kullanıcısının GitHub profili indiriliyor...{RENK_SIYAH}")
    user_data = github_api_get(f"https://api.github.com/users/{kullanici_adi}")
    
    if not user_data or 'login' not in user_data:
        print(f"{RENK_KIRMIZI}[HATA]: Kullanıcı bulunamadı.{RENK_SIYAH}")
        return False
        
    profil_ozeti = f"""
    --- GITHUB PROFİL BİLGİLERİ ---
    Kullanıcı Adı: {user_data.get('login')}
    Gerçek İsim: {user_data.get('name', 'Belirtilmemiş')}
    Biyografi: {user_data.get('bio', 'Yok')}
    Şirket: {user_data.get('company', 'Yok')}
    Konum: {user_data.get('location', 'Yok')}
    Halka Açık Repo Sayısı: {user_data.get('public_repos')}
    Takipçi: {user_data.get('followers')} | Takip Edilen: {user_data.get('following')}
    Hesap Oluşturma: {user_data.get('created_at')}
    """
    
    print(f"  Repolar listeleniyor...")
    repos_data = github_api_get(f"https://api.github.com/users/{kullanici_adi}/repos?sort=updated&per_page=30")
    
    repo_ozeti = "\n    --- SAHİP OLUNAN REPOLAR ---\n"
    if repos_data and isinstance(repos_data, list):
        for repo in repos_data:
            dil = repo.get('language', 'Bilinmiyor')
            yildiz = repo.get('stargazers_count', 0)
            aciklama = repo.get('description', 'Açıklama yok')
            isim = repo.get('name')
            repo_ozeti += f"    - {isim} | Dil: {dil} | Yıldız: {yildiz} | Açıklama: {aciklama}\n"
    else:
        repo_ozeti += "    (Repo bulunamadı veya API limiti aşıldı)\n"

    tum_baglam = profil_ozeti + repo_ozeti
    hafiza_mesaji = f"Aşağıda '{kullanici_adi}' kullanıcısının GitHub profil detayları bulunmaktadır. Bundan sonraki sorularında bu bilgileri kullan:\n{tum_baglam}"
    
    sohbet_gecmisi.append({"role": "system", "content": hafiza_mesaji})
    print(f"{RENK_YESIL}[SİSTEM]: Başarılı! Profil ve repolar hafızaya alındı.{RENK_SIYAH}\n")
    return True

def github_repoyu_hafizaya_al(repo):
    # Belirli bir repodaki dosyaları çeken fonksiyon
    print(f"\n{RENK_SARI}[SİSTEM]: '{repo}' reposu okunuyor...{RENK_SIYAH}")
    proje_baglami = ""
    
    url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    data = github_api_get(url)
    
    if not data or 'tree' not in data:
        data = github_api_get(f"https://api.github.com/repos/{repo}/git/trees/master?recursive=1")
        if not data or 'tree' not in data:
            print(f"{RENK_KIRMIZI}[HATA]: Repo bulunamadı veya dal (branch) okunamadı.{RENK_SIYAH}")
            return False
            
    dosyalar = [item['path'] for item in data['tree'] if item['path'].endswith(('.py', '.md', '.txt')) and 'test' not in item['path']]
    dosyalar = dosyalar[:3] 
    
    if not dosyalar:
        print(f"{RENK_SARI}[HATA]: Bu repoda okunacak dosya bulunamadı.{RENK_SIYAH}")
        return False
        
    for dosya in dosyalar:
        print(f"  İndiriliyor: {dosya}")
        file_url = f"https://api.github.com/repos/{repo}/contents/{dosya}"
        file_data = github_api_get(file_url)
        
        if file_data and 'content' in file_data:
            icerik = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
            proje_baglami += f"\n--- DOSYA: {dosya} ---\n{icerik[:3000]}\n"
            
    hafiza_mesaji = f"Aşağıdaki dosyalar '{repo}' reposuna aittir. Bu içerikleri bilerek cevap ver:\n{proje_baglami}"
    sohbet_gecmisi.append({"role": "system", "content": hafiza_mesaji})
    
    print(f"{RENK_YESIL}[SİSTEM]: Başarılı! {len(dosyalar)} dosya hafızaya alındı.{RENK_SIYAH}\n")
    return True

def yapay_zeka_ile_sohbet_et(kullanici_mesaji, api_key):
    # Groq API'sine istek atan ana fonksiyon
    sohbet_gecmisi.append({"role": "user", "content": kullanici_mesaji})
    url = "https://api.groq.com/openai/v1/chat/completions" 
    data = {
        "model": "openai/gpt-oss-120b", 
        "messages": sohbet_gecmisi,
        "temperature": 0.7
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method='POST')
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        with urllib.request.urlopen(req) as response:
            sonuc = json.loads(response.read().decode())
            cevap = sonuc['choices'][0]['message']['content']
            sohbet_gecmisi.append({"role": "assistant", "content": cevap})
            return cevap
    except Exception as e:
        return f"Sistemsel hata: {e}"

def arayuzu_baslat():
    # Ana döngü (Kullanıcıdan komut alır)
    ekrani_temizle()
    print(RENK_MAVI + "="*55)
    print(f"{RENK_YESIL}    🧠 DEEP AI ASİSTANI (Gelişmiş Okuma Modu)    ")
    print(RENK_MAVI + "="*55 + RENK_SIYAH)
    print("💡 Komutlar:")
    print("   /profil kullanici_adi  -> Tüm profil ve repoları öğrenir")
    print("   /github kullanici/repo -> Repodaki dosyaları okur")
    print("Çıkmak için 'q' yazıp Enter'a basın.\n")
    
    while True:
        try:
            kullanici_girdisi = input(RENK_MAVI + "🧑 Sen: " + RENK_SIYAH)
            
            if kullanici_girdisi.lower() in ['q', 'çıkış', 'exit']:
                print(RENK_YESIL + "\n🤖 Asistan: Görüşmek üzere!" + RENK_SIYAH)
                break
                
            if not kullanici_girdisi.strip():
                continue
                
            if kullanici_girdisi.startswith("/profil "):
                kullanici_adi = kullanici_girdisi.replace("/profil ", "").strip()
                github_profilini_hafizaya_al(kullanici_adi)
                continue 
                
            if kullanici_girdisi.startswith("/github "):
                repo_adi = kullanici_girdisi.replace("/github ", "").strip()
                repo_adi = repo_adi.replace("https://github.com/", "").replace(".git", "")
                github_repoyu_hafizaya_al(repo_adi)
                continue 
                
            print(RENK_YESIL + "🤖 Asistan: " + RENK_SIYAH, end="", flush=True)
            time.sleep(0.5)
            cevap = yapay_zeka_ile_sohbet_et(kullanici_girdisi, GROQ_API_KEY)
            print(cevap + "\n")
            
        except KeyboardInterrupt:
            print("\n" + RENK_YESIL + "🤖 Asistan: Görüşmek üzere!" + RENK_SIYAH)
            break
        except Exception as e:
            print(f"\n{RENK_KIRMIZI}Bir hata oluştu: {e}{RENK_SIYAH}")

if __name__ == "__main__":
    arayuzu_baslat()