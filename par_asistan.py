#!/usr/bin/env python3
import time

from colorama import Fore, Style, init
from pyfiglet import Figlet

import sistem_kontrol


def renkli_baslik(ekran_temizle=True):
    init(autoreset=True)
    if ekran_temizle:
        sistem_kontrol.clear_screen()

    figlet = Figlet(font="slant")
    renkler = (Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.GREEN, Fore.YELLOW)

    for index, line in enumerate(figlet.renderText("ParAsistan").splitlines()):
        print(Style.BRIGHT + renkler[index % len(renkler)] + line)

    print(Fore.WHITE + Style.BRIGHT + "Pardus Terminal ParAsistan")
    print(Style.DIM + time.strftime("%d.%m.%Y %H:%M:%S"))
    print()


def komutlari_goster():
    print(Fore.CYAN + Style.BRIGHT + "Komutlar")
    print(Fore.GREEN + "  sistem_kontrol" + Style.RESET_ALL + "  Sistem durumunu gosterir")
    print(Fore.RED + "  exit" + Style.RESET_ALL + "            Cikis yapar")
    print()


def sistem_durumunu_goster():
    renkli_baslik()
    sistem_kontrol.sistem_kontrol(baslik_goster=False, ekran_temizle=False)
    input(Fore.WHITE + Style.DIM + "\nMenuye donmek icin Enter'a basin...")


def main():
    while True:
        renkli_baslik()
        komutlari_goster()

        komut = input(Fore.WHITE + Style.BRIGHT + "ParAsistan> " + Style.RESET_ALL).strip().lower()

        if komut == "sistem_kontrol":
            sistem_durumunu_goster()
        elif komut == "exit":
            print(Fore.YELLOW + "ParAsistan kapatiliyor...")
            break
        elif not komut:
            continue
        else:
            print(Fore.RED + "Bilinmeyen komut: " + komut)
            input(Fore.WHITE + Style.DIM + "Devam etmek icin Enter'a basin...")


if __name__ == "__main__":
    main()
