PuthonIDE
=========

iOS uzerinde calisan, terminal tabanli
yapay zeka asistani. Groq API ile
sohbet eder, GitHub repolarini ve
profilleri analiz eder.

Ozellikler
----------
- Groq AI ile dogal dil sohbeti
- /github kullanici/repo komutu ile
  proje bilgilerini cekme ve hafizaya alma
- /profil kullanici komutu ile GitHub
  profili ve repolarini goruntuleme
- iSH (iOS) uyumlu, ek pakete gerek yok
- Renkli terminal arayuzu
- Sohbet gecmisi (son 20 mesaj)

Kurulum
-------
1. iSH uygulamasini App Store'dan indir
2. Terminalde su komutlari calistir:

   apk add git python3

3. Repoyu klonla:

   git clone
   https://github.com/Okanzncr/PuthonIDE.git
   cd PuthonIDE

4. API anahtari ekle:

   egeny.py dosyasini ac ve su satira
   kendi Groq API anahtarini yaz:

   GROQ_API_KEY = "gsk_..."

   (Anahtar almak icin:
   console.groq.com adresine git)

Calistirma
----------
python3 main.py

veya

python3 egeny.py

Komutlar
--------
/github kullanici/repo
  Belirtilen repoyu hafizaya alir,
  aciklama ve yildiz sayisini gosterir.

/profil kullanici_adi
  GitHub profilini ve ilk 5 reposunu
  listeler.

cikis veya exit
  Programdan cikar.

Gereksinimler
-------------
- iOS 14 veya uzeri
- iSH uygulamasi
- Internet baglantisi
- Groq API anahtari (ucretsiz)

Lisans
------
Bu proje acik kaynak kodludur.
