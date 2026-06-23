# ParAsistan

Pardus icin terminalde CPU, RAM, disk ve sicaklik bilgisini gosteren basit bir Python asistan uygulamasi.

## Ozellikler

- CPU kullanimini gosterir.
- RAM kullanimini gosterir.
- Disk kullanimini gosterir.
- Uygun sensor varsa sicaklik bilgisini gosterir.
- Terminalde renkli ve okunabilir bir arayuz sunar.

## Kurulum

Projeyi indirin:

```bash
git clone https://github.com/umutumutumutumut/ParAsistan.git
cd ParAsistan
```

Gerekli paketleri kurun:

```bash
python3 kurulum.py
```

Kurulum hata verirse Pardus terminalde elle sunu deneyin:

```bash
sudo apt install python3-colorama python3-pyfiglet
```

## Calistirma

```bash
python3 par_asistan.py
```

## Dosyalar

- `par_asistan.py`: Uygulamayi baslatan ana dosya.
- `sistem_kontrol.py`: Sistem bilgilerini gosteren modul.
- `kurulum.py`: Gerekli Python paketlerini kuran yardimci dosya.
