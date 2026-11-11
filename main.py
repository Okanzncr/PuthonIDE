import sys
import os

def dosya_kontrol(dosya_adi):
    # Gerekli dosyanın var olup olmadığını kontrol eder
    return os.path.exists(dosya_adi)

def ana_program():
    # Gerekli dosyayı kontrol et
    if not dosya_kontrol("egeny.py"):
        print("\n[HATA]: 'egeny.py' bulunamadi!")
        print("Lutfen su dosyalarin ayni klasorde oldugundan emin olun:")
        print("  - main.py")
        print("  - egeny.py")
        print("\nProgram kapatiliyor...")
        sys.exit(1)

    try:
        # egeny.py icindeki arayuzu ice aktar
        from egeny import arayuzu_baslat

        print("=" * 55)
        print("PuthonIDE baslatiliyor...")
        print("Yapay Zeka Asistani yukleniyor, lutfen bekleyin.")
        print("=" * 55)
        print()

        # Asistani calistir
        arayuzu_baslat()

    except ImportError as e:
        print(f"\n[IMPORT HATASI]: Modulu yuklerken sorun olustu: {e}")
        print("egeny.py dosyasi bozuk veya eksik olabilir.")

    except AttributeError:
        print("\n[HATA]: 'arayuzu_baslat' fonksiyonu egeny.py icinde bulunamadi!")
        print("Lutfen egeny.py dosyasini kontrol edin.")

    except KeyboardInterrupt:
        print("\n\nProgram kullanici tarafindan kapatildi (Ctrl+C).")
        print("Gorusmek uzere!")

    except Exception as e:
        print(f"\n[BEKLENMEYEN HATA]: {type(e).__name__}: {e}")
        print("Lutfen bu hatayi gelistiriciye bildirin.")

if __name__ == "__main__":
    # Programi baslat
    ana_program()
---
