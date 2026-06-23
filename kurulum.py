#!/usr/bin/env python3
import importlib.util
import shutil
import subprocess
import sys


PACKAGES = {
    "colorama": "python3-colorama",
    "pyfiglet": "python3-pyfiglet",
}


def installed(module_name):
    return importlib.util.find_spec(module_name) is not None


def run(command):
    print("Calistiriliyor:", " ".join(command))
    subprocess.check_call(command)


def install_with_pip(module_name):
    run([sys.executable, "-m", "pip", "install", "--user", module_name])


def install_with_apt(apt_packages):
    if shutil.which("sudo"):
        command = ["sudo", "apt", "install", "-y", *apt_packages]
    else:
        command = ["apt", "install", "-y", *apt_packages]
    run(command)


def main():
    missing = [module for module in PACKAGES if not installed(module)]
    if not missing:
        print("Gerekli paketler zaten yuklu.")
        return 0

    print("Eksik paketler:", ", ".join(missing))

    try:
        install_with_pip(missing[0])
        for module in missing[1:]:
            install_with_pip(module)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pip ile kurulum basarisiz oldu, apt deneniyor...")
        apt_packages = [PACKAGES[module] for module in missing]
        try:
            install_with_apt(apt_packages)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print()
            print("Kurulum tamamlanamadi.")
            print("Pardus terminalde elle sunu deneyin:")
            print("sudo apt install python3-colorama python3-pyfiglet")
            return 1

    still_missing = [module for module in PACKAGES if not installed(module)]
    if still_missing:
        print("Bazi paketler hala bulunamiyor:", ", ".join(still_missing))
        return 1

    print("Kurulum tamamlandi.")
    print("Simdi calistirin: python3 par_asistan.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
