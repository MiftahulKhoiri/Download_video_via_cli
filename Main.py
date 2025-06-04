import urllib.request
import sys
import os
import subprocess
from time import sleep

def hapus_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def auto_update_script():
    hapus_layar()
    print("Melakukan pengecekan script ...")
    sleep(1)
    url = 'https://raw.githubusercontent.com/MiftahulKhoiri/Download_video_via_cli/main/Main.py'
    local_file = os.path.abspath(__file__)
    try:
        with urllib.request.urlopen(url) as response:
            new_code = response.read()
        with open(local_file, 'rb') as f:
            current_code = f.read()
        if current_code != new_code:
            print("🔄 Terdapat pembaruan script tersedia di GitHub.")
            jawab = input("Apakah Anda ingin memperbarui script sekarang? (y/n): ")
            if jawab.lower() == "y":
                with open(local_file, 'wb') as f:
                    f.write(new_code)
                print("✅ Script sudah diperbarui! Silakan jalankan ulang script ini.")
                sys.exit(0)
            else:
                print("Lewati pembaruan. Anda menjalankan versi lokal.")
        else:
            print("Script sudah versi terbaru.\n")
    except Exception as e:
        print(f"Gagal memeriksa pembaruan: {e}")

def cek_dan_install_modul():
    import importlib.util

    def install_if_needed(module_name, pip_name=None):
        if pip_name is None:
            pip_name = module_name
        if importlib.util.find_spec(module_name) is None:
            print(f"Modul '{module_name}' belum terinstall, menginstall ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"Modul '{module_name}' sudah terinstall.")
        else:
            print(f"Modul '{module_name}' sudah terinstall.")

    install_if_needed("yt_dlp")
    install_if_needed("colorama")
    # ffmpeg tidak bisa diinstall via pip, cek via command line
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("ffmpeg sudah terinstall.")
    except Exception:
        print("ffmpeg belum terinstall. Silakan install manual sesuai OS Anda (lihat https://www.gyan.dev/ffmpeg/builds/ untuk Windows).")

# Jalankan auto update lalu cek & install modul
auto_update_script()
cek_dan_install_modul()

# Setelah dipastikan, baru import modul yang dibutuhkan
import yt_dlp
from colorama import Fore, Style, init
init(autoreset=True)

def print_header():
    print(Fore.CYAN + Style.BRIGHT)
    print("╔" + "═"*38 + "╗")
    print("║   🚀  WEB VIDEO DOWNLOAD CLI  🚀   ║")
    print("╚" + "═"*38 + "╝")
    print(Style.RESET_ALL)

def buat_folder_download():
    folder = "web_video_download"
    os.makedirs(folder, exist_ok=True)
    return folder

def pilih_platform():
    hapus_layar()
    print_header()
    print("╔══════════════════════════╗")
    print("║   PILIH PLATFORM VIDEO   ║")
    print("╠══════════════════════════╣")
    print("║ 1. YouTube               ║")
    print("║ 2. Facebook              ║")
    print("║ 3. Twitter               ║")
    print("║ 4. Keluar                ║")
    print("╚══════════════════════════╝")
    while True:
        pilihan = input("Masukkan pilihan (1-4): ")
        if pilihan in ['1', '2', '3', '4']:
            return pilihan
        print(Fore.RED + "Pilihan tidak valid! Silakan pilih 1-4")

def pilih_mode_download():
    print("\n╔══════════════════════════╗")
    print("║        PILIH MODE        ║")
    print("╠══════════════════════════╣")
    print("║ 1. Download Satu Video   ║")
    print("║ 2. Download Banyak Video ║")
    print("╚══════════════════════════╝")
    while True:
        mode = input("Masukkan pilihan (1-2): ")
        if mode in ['1', '2']:
            return mode
        print(Fore.RED + "Pilihan tidak valid! Silakan pilih 1-2")

def pilih_resolusi(url):
    hapus_layar()
    print(Fore.YELLOW + "Mengambil informasi video...")
    ydl_opts = {'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [f for f in info['formats']
                       if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            if not formats:
                print(Fore.RED + "Tidak ada format video+audio yang tersedia")
                return None, None, None
            if len(formats) == 1:
                fmt = formats[0]
                res = fmt.get('resolution', 'Unknown')
                ext = fmt.get('ext', 'Unknown')
                print(Fore.YELLOW + f"\nINFO: Hanya ada 1 resolusi ({res}, {ext}). Download otomatis...")
                sleep(2)
                return fmt['format_id'], res, ext
            print("\n╔══════════════════════════════╗")
            print("║      PILIH RESOLUSI VIDEO    ║")
            print("╠══════════════════════════════╣")
            for i, fmt in enumerate(formats):
                res = fmt.get('resolution', 'Unknown')
                ext = fmt.get('ext', 'Unknown')
                print(f"║ {i+1}. {res.ljust(8)} ({ext.ljust(5)}) ║")
            print("╚══════════════════════════════╝")
            while True:
                pilihan = input("\nPilih resolusi (nomor, atau Enter untuk batal): ").strip()
                if pilihan == "":
                    print(Fore.YELLOW + "Batal memilih resolusi.")
                    return None, None, None
                try:
                    idx = int(pilihan) - 1
                    if 0 <= idx < len(formats):
                        res = formats[idx].get('resolution', 'Unknown')
                        ext = formats[idx].get('ext', 'Unknown')
                        return formats[idx]['format_id'], res, ext
                    print(Fore.RED + "Nomor tidak valid!")
                except ValueError:
                    print(Fore.RED + "Harap masukkan angka!")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        return None, None, None

def cek_file_sudah_ada(url, folder):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            nama_file = ydl.prepare_filename(info)
            path_lengkap = os.path.join(folder, os.path.basename(nama_file))
            return os.path.exists(path_lengkap)
    except:
        return False

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '?').strip()
        bar_len = 30
        try:
            val = float(percent.replace('%',''))
            filled_len = int(round(bar_len * val / 100))
        except:
            filled_len = 0
        bar = '#' * filled_len + '-' * (bar_len - filled_len)
        print(f"\r{Fore.CYAN}[{bar}] {percent} selesai", end='', flush=True)
    elif d['status'] == 'finished':
        print(Fore.GREEN + "\nProses download selesai!".ljust(50))

def download_video(url, folder, format_id=None):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            path_lengkap = os.path.join(folder, os.path.basename(filename))
    except Exception:
        filename = None
        path_lengkap = None

    if cek_file_sudah_ada(url, folder):
        print(Fore.YELLOW + "\n⚠ Video sudah ada di folder download")
        return "exists", path_lengkap

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if not format_id else format_id,
        'outtmpl': f'{folder}/%(title)s-%(id)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(Fore.GREEN + "\n✓ Download berhasil!")
            filename = ydl.prepare_filename(info)
            path_lengkap = os.path.join(folder, os.path.basename(filename))
            return "success", path_lengkap
    except Exception as e:
        print(Fore.RED + f"\n✗ Gagal download: {e}")
        import traceback
        traceback.print_exc()
        return "failed", None

def download_banyak_terbaik(folder, platform_domains):
    urls = []
    hasil_download = []
    print(Fore.LIGHTBLUE_EX + "Masukkan alamat URL video satu per satu.")
    print(Fore.LIGHTBLUE_EX + "Jika sudah selesai, cukup tekan Enter tanpa mengetik apa-apa.")
    while True:
        url = input("Alamat = ").strip()
        if url == "":
            break
        if not any(domain in url for domain in platform_domains):
            print(Fore.RED + f"URL tidak valid! Pastikan URL dari {', '.join(platform_domains)}")
            continue
        urls.append(url)
    if not urls:
        print(Fore.YELLOW + "Tidak ada alamat yang dimasukkan.")
        input("Tekan Enter untuk kembali ke menu utama...")
        return
    print(Fore.YELLOW + f"\nMulai mendownload {len(urls)} video secara otomatis (format terbaik)...\n")
    for i, url in enumerate(urls, 1):
        print(Fore.CYAN + f"\n[{i}/{len(urls)}] Download: {url}")
        result, filename = download_video(url, folder)
        hasil_download.append((result, filename))
'No.':<4} {'Nama File':<35} Status")
    for idx, (status, fname) in enumerate(hasil_download, 1):
        warna = Fore.GREEN if status == "success" else (Fore.YELLOW if status == "exists" else Fore.RED)
        fname_disp = os.path.basename(fname) if fname else "-"
        print(f"{idx:<4} {fname_disp:<35} {warna}{status}")
    print(Fore.LIGHTBLACK_EX + "-"*60)
    print(Fore.LIGHTBLUE_EX + "\nSEMUA PROSES SELESAI.")
    input(Fore.LIGHTBLUE_EX + "Tekan Enter untuk kembali ke menu utama...")

def main():
    hapus_layar()
    print_header()
    print(Fore.YELLOW + "Mendapatkan informasi modul yang dibutuhkan ...")
    sleep(1)
    hapus_layar()
    print_header()
    print(Fore.GREEN + Style.BRIGHT + "SELAMAT DATANG DI APLIKASI")
    print(Fore.CYAN + "   ○ WEB VIDEO DOWNLOAD ○")
    print(Fore.LIGHTBLACK_EX + "-" * 40)
    print(Fore.LIGHTBLUE_EX + "Tips: Gunakan mode banyak video untuk batch download playlist!")
    sleep(1)
    folder = buat_folder_download()

    platforms = {
        '1': ['youtube.com', 'youtu.be'],
        '2': ['facebook.com', 'fb.watch'],
        '3': ['twitter.com', 'x.com']
    }

    while True:
        pilihan = pilih_platform()
        if pilihan == '4':
            print(Fore.GREEN + "\nTerima kasih telah menggunakan program ini!")
            break

        mode = pilih_mode_download()
        if mode == '1':
            while True:
                hapus_layar()
                print_header()
                url = input("Masukkan URL video: ").strip()
                if not url:
                    print(Fore.RED + "URL tidak boleh kosong!")
                    sleep(1)
                    continue
                if any(domain in url for domain in platforms[pilihan]):
                    break
                print(Fore.RED + f"URL tidak valid! Pastikan URL dari {', '.join(platforms[pilihan])}")
                sleep(1)
            format_id = None
            res = None
            ext = None
            if pilihan in ['1', '2']:
                format_id, res, ext = pilih_resolusi(url)
                if not format_id:
                    input(Fore.YELLOW + "Tekan Enter untuk kembali...")
                    continue
                print(Fore.YELLOW + f"\nDownload dimulai untuk resolusi: {res}, format: {ext}")
                sleep(1)
            hapus_layar()
            print(Fore.CYAN + "Memulai download...")
            result, filename = download_video(url, folder, format_id)
            if result == "success":
                print(Fore.GREEN + f"File tersimpan di: {filename}")
            elif result == "exists":
                print(Fore.YELLOW + f"File sudah ada di folder download: {filename}")
            input(Fore.LIGHTBLUE_EX + "Tekan Enter untuk kembali ke menu utama...")
        else:
            hapus_layar()
            print_header()
            print(Fore.CYAN + "MODE DOWNLOAD BANYAK VIDEO")
            download_banyak_terbaik(folder, platforms[pilihan])

if __name__ == "__main__":
    main()