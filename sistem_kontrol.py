#!/usr/bin/env python3
import os
import shutil
import time
from pathlib import Path

from colorama import Fore, Style, init
from pyfiglet import Figlet


def format_bytes(value):
    units = ("B", "KB", "MB", "GB", "TB")
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024


def read_cpu_times():
    if not Path("/proc/stat").exists():
        return None

    with open("/proc/stat", "r", encoding="utf-8") as proc_stat:
        fields = proc_stat.readline().split()[1:]

    values = [int(field) for field in fields]
    idle = values[3] + values[4]
    total = sum(values)
    return idle, total


def cpu_usage_percent():
    if not Path("/proc/stat").exists():
        try:
            load_1m = os.getloadavg()[0]
            cpu_count = os.cpu_count() or 1
            return max(0.0, min(100.0, load_1m / cpu_count * 100))
        except OSError:
            return None

    idle_a, total_a = read_cpu_times()
    time.sleep(0.35)
    idle_b, total_b = read_cpu_times()

    idle_delta = idle_b - idle_a
    total_delta = total_b - total_a
    if total_delta <= 0:
        return 0.0

    return max(0.0, min(100.0, (1 - idle_delta / total_delta) * 100))


def ram_status():
    if not Path("/proc/meminfo").exists():
        return None

    values = {}
    with open("/proc/meminfo", "r", encoding="utf-8") as meminfo:
        for line in meminfo:
            key, raw_value = line.split(":", 1)
            values[key] = int(raw_value.strip().split()[0]) * 1024

    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", 0)
    used = total - available
    percent = (used / total * 100) if total else 0
    return total, used, percent


def disk_status(path="/"):
    usage = shutil.disk_usage(path)
    percent = (usage.used / usage.total * 100) if usage.total else 0
    return usage.total, usage.used, percent


def temperature_status():
    names = ("x86_pkg_temp", "coretemp", "k10temp", "acpitz", "thermal_zone")
    candidates = []

    for temp_file in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
        type_file = temp_file.with_name("type")
        sensor_name = type_file.read_text(encoding="utf-8").strip() if type_file.exists() else ""
        priority = next((index for index, name in enumerate(names) if name in sensor_name), len(names))
        candidates.append((priority, temp_file))

    for _, temp_file in sorted(candidates):
        try:
            raw_value = int(temp_file.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            continue

        temp = raw_value / 1000 if raw_value > 1000 else raw_value
        if -20 <= temp <= 125:
            return temp

    return None


def color_for_percent(percent):
    if percent is None:
        return Fore.WHITE
    if percent < 60:
        return Fore.GREEN
    if percent < 85:
        return Fore.YELLOW
    return Fore.RED


def progress_bar(percent, width=28):
    filled = round(width * percent / 100)
    empty = width - filled
    color = color_for_percent(percent)
    return f"{color}{'█' * filled}{Style.DIM}{'░' * empty}{Style.RESET_ALL}"


def row(label, value, percent=None):
    if percent is None:
        bar = f"{Style.DIM}{'░' * 28}{Style.RESET_ALL}"
        percent_text = "   -"
    else:
        bar = progress_bar(percent)
        percent_text = f"{percent:5.1f}%"

    return f"{Fore.CYAN}{label:<10}{Style.RESET_ALL} {bar} {percent_text}  {value}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def sistem_kontrol():
    init(autoreset=True)
    clear_screen()

    figlet = Figlet(font="slant")
    print(Fore.BLUE + figlet.renderText("ParAsistan"))
    print(Fore.WHITE + Style.BRIGHT + "Pardus Terminal ParAsistan")
    print(Style.DIM + time.strftime("%d.%m.%Y %H:%M:%S"))
    print()

    cpu_percent = cpu_usage_percent()
    ram = ram_status()
    disk_total, disk_used, disk_percent = disk_status("/")
    temperature = temperature_status()

    print(row("CPU", "islemci kullanimi" if cpu_percent is not None else "bilgi alinamadi", cpu_percent))
    if ram is None:
        print(row("RAM", "bilgi alinamadi"))
    else:
        ram_total, ram_used, ram_percent = ram
        print(row("RAM", f"{format_bytes(ram_used)} / {format_bytes(ram_total)}", ram_percent))
    print(row("DISK", f"{format_bytes(disk_used)} / {format_bytes(disk_total)}", disk_percent))

    if temperature is None:
        print(row("SICAKLIK", "sensor bulunamadi"))
    else:
        temp_color = Fore.GREEN if temperature < 65 else Fore.YELLOW if temperature < 85 else Fore.RED
        print(row("SICAKLIK", f"{temp_color}{temperature:.1f} C{Style.RESET_ALL}"))

    print()
    print(Style.DIM + "Tekrar gormek icin komutu yeniden calistirin.")


def main():
    sistem_kontrol()


if __name__ == "__main__":
    main()
