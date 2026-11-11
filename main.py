# main.py - Projenin Ana Giriş Noktası

def ana_program():
    try:
        # egeny.py dosyasındaki asistan arayüzünü içe aktar
        from egeny import arayuzu_baslat
        
        print("="*55)
        print("Sistem başlatılıyor... Yapay Zeka Asistanı yükleniyor.")
        print("="*55 + "\n")
        
        # Asistanı çalıştır
        arayuzu_baslat()
        
    except ImportError:
        print("\n[HATA]: 'egeny.py' dosyası bulunamadı!")
        print("Lütfen 'main.py' ve 'egeny.py' dosyalarının aynı klasörde olduğundan emin olun.")
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından kapatıldı.")
    except Exception as e:
        print(f"\nBeklenmeyen bir hata oluştu: {e}")

# Dosya doğrudan çalıştırıldığında ana_program fonksiyonunu başlat
if __name__ == "__main__":
    ana_program()