# Copyright (c) 2026 Farid Suryadi
# All Rights Reserved.

import os
import sys
import time
import itertools
import subprocess

# ── Warna ANSI ──
G = "\033[92m"   # Hijau
B = "\033[94m"   # Biru
Y = "\033[93m"   # Kuning
R = "\033[91m"   # Merah
W = "\033[97m"   # Putih
BD = "\033[1m"   # Bold
RS = "\033[0m"   # Reset

BANNER = r"""
 __  __             _     _              _                       _
|  \/  | __ _  ___| |__ (_)_ __  ___  | |    ___  __ _ _ __ _ __ (_)_ __   __ _
| |\/| |/ _` |/ __| '_ \| | '_ \ / _ \ | |   / _ \/ _` | '__| '_ \| | '_ \ / _` |
| |  | | (_| | (__| | | | | | | |  __/ | |__|  __/ (_| | |  | | | | | | | | (_| |
|_|  |_|\__,_|\___|_| |_|_|_| |_|\___| |_____\___|\__,_|_|  |_| |_|_|_| |_|\__, |
                                                                            |___/
"""

# BASE_DIR sekarang bukan __file__, tapi folder user menjalankan program
BASE_DIR = os.path.abspath(os.getcwd())


def set_base_dir(path=None):
    """Set folder base untuk mencari lab-*."""
    global BASE_DIR

    if path and os.path.isdir(path):
        BASE_DIR = os.path.abspath(path)
    else:
        BASE_DIR = os.path.abspath(os.getcwd())


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def loading(msg, duration=1.5):
    """Animasi spinner."""
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    end = time.time() + duration
    print(f"\n{Y}{BD}>> {msg}", end="", flush=True)
    while time.time() < end:
        sys.stdout.write(f" {G}{next(spinner)}{RS}")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b\b")
    print(f" {G}[DONE]{RS}\n")


def get_labs():
    """Mencari folder lab."""
    if not os.path.isdir(BASE_DIR):
        return []

    return sorted(
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d)) and d.startswith("lab-")
    )


def get_scripts(lab_folder):
    """Mencari file python dalam folder scripts."""
    scripts_dir = os.path.join(BASE_DIR, lab_folder, "scripts")
    if not os.path.isdir(scripts_dir):
        return []
    return sorted(f for f in os.listdir(scripts_dir) if f.endswith(".py"))


def prettify(filename):
    """Ubah nama file dari script_name.py ke Script Name."""
    return filename.replace(".py", "").replace("_", " ").title()


def get_python(lab):
    """Cari venv python di dalam folder lab, fallback ke sys.executable."""
    if os.name == "nt":
        venv = os.path.join(BASE_DIR, lab, ".venv", "Scripts", "python.exe")
    else:
        venv = os.path.join(BASE_DIR, lab, ".venv", "bin", "python")
    return venv if os.path.exists(venv) else sys.executable


def create_lab():
    """Membuat folder lab-XX dan scripts secara otomatis."""
    clear()
    print(f"\n{G}{BD}  ╔{'═' * 40}╗{RS}")
    print(f"{G}{BD}  ║{'CREATE NEW LAB':^40}║{RS}")
    print(f"{G}{BD}  ╚{'═' * 40}╝{RS}\n")

    print(f"{Y}Base Directory:{RS} {W}{BASE_DIR}{RS}\n")

    num = input(f"{BD} Masukkan Nomor Lab (contoh: 3, 04, 12): {RS}").strip()

    if not num.isdigit():
        print(f"\n{R}[!] Gagal: Masukkan angka yang valid.{RS}")
        time.sleep(1.5)
        return

    lab_folder = f"lab-{int(num):02d}"
    lab_path = os.path.join(BASE_DIR, lab_folder)
    scripts_path = os.path.join(lab_path, "scripts")

    if os.path.exists(lab_path):
        print(f"\n{Y}[!] Folder '{lab_folder}' sudah ada!{RS}")
    else:
        os.makedirs(scripts_path, exist_ok=True)
        print(f"\n{G}[+] Berhasil membuat folder: {lab_folder}{RS}")
        print(f"{G}[+] Berhasil membuat folder: {lab_folder}/scripts{RS}")

    time.sleep(2)


def lab_menu(lab_folder):
    """Menu khusus untuk isi di dalam lab yang dipilih"""
    lab_name = lab_folder.upper().replace("-", " ")

    while True:
        clear()
        print(f"\n{G}{BD}  ╔{'═' * 40}╗{RS}")
        print(f"{G}{BD}  ║  {lab_name:^36}  ║{RS}")
        print(f"{G}{BD}  ╚{'═' * 40}╝{RS}\n")

        print(f"{Y}Base Directory:{RS} {W}{BASE_DIR}{RS}\n")

        scripts = get_scripts(lab_folder)

        if not scripts:
            print(f"  {Y}[!] Tidak ada script di folder '{lab_folder}/scripts/'.{RS}")
            print(f"  {Y}    Silakan buat foldernya dan tambahkan file .py{RS}\n")

        print(f"{B}{'=' * 55}{RS}")
        print(f"{BD}  LIST OF SCRIPTS ({lab_name}):{RS}")

        for i, filename in enumerate(scripts, 1):
            print(f"  {G}{BD}[{i}]{RS} {prettify(filename)}")

        print(f"  {R}{BD}[0]{RS} Kembali ke Menu Utama")
        print(f"{B}{'=' * 55}{RS}")

        choice = input(f"{BD} Pilih: {RS}").strip()

        if choice == "0":
            break

        if not choice.isdigit():
            print(f"\n{R}Masukkan angka yang valid!{RS}")
            time.sleep(1)
            continue

        idx = int(choice) - 1

        if 0 <= idx < len(scripts):
            filename = scripts[idx]
            path = os.path.join(BASE_DIR, lab_folder, "scripts", filename)

            print(f"\n{Y}>>> Running: {prettify(filename)}...{RS}")
            print(f"{B}{'-' * 55}{RS}")

            try:
                subprocess.run([get_python(lab_folder), path], check=True)
            except Exception as e:
                print(f"\n{R}[Error] Gagal menjalankan: {e}{RS}")

            print(f"{B}{'-' * 55}{RS}")
            input(f"\n{Y}Selesai. Tekan Enter untuk kembali...{RS}")
        else:
            print(f"\n{R}Opsi tidak tersedia!{RS}")
            time.sleep(1)


def main():
    # set base dir otomatis dari folder user menjalankan command
    set_base_dir()

    while True:
        clear()
        print(f"{G}{BD}{BANNER}{RS}")
        print(f"{W}{BD}                     Copyright (c) 2026 Farid Suryadi{RS}\n")
        print(f"{Y}Base Directory:{RS} {W}{BASE_DIR}{RS}\n")

        print(f"{B}{'=' * 70}{RS}")
        print(f"{BD} SELECT LAB:{RS}")

        labs = get_labs()

        if not labs:
            print(f"  {Y}[!] Tidak ada folder lab ditemukan di:{RS}")
            print(f"  {W}{BASE_DIR}{RS}\n")

        for i, lab in enumerate(labs, 1):
            print(f"  {G}[{i}]{RS} {lab.upper().replace('-', ' ')}")

        print(f"  {Y}[c]{RS} Create New Lab")
        print(f"  {Y}[0]{RS} Exit")
        print(f"{B}{'=' * 70}{RS}")

        choice = input(f"{BD} Pilih: {RS}").strip().lower()

        if choice == "0":
            print(f"\n{Y}Bye!{RS}")
            break

        if choice == "c":
            create_lab()
            continue

        if not choice.isdigit():
            print(f"{R}[!] Masukkan angka yang valid.{RS}")
            time.sleep(1)
            continue

        idx = int(choice) - 1

        if not (0 <= idx < len(labs)):
            print(f"{R}[!] Opsi tidak tersedia.{RS}")
            time.sleep(1)
            continue

        lab_folder = labs[idx]
        loading(f"Membuka {lab_folder.upper()}")
        lab_menu(lab_folder)


def run():
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Program dihentikan.{RS}")
