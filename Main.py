import urllib.request
import sys
import os
import subprocess
from time import sleep

def auto_update_script():
    hapus_layar()
    print (" melakukan pengecekan script ")
    sleep(2)
    url = 'https://raw.githubusercontent.com/MiftahulKhoiri/Download_video_via_cli/main/Main.py'
    local_file = os.path.abspath(__file__)
    try:
        with urllib.request.urlopen(url) as response:
            new_code = response.read()
        with open(local_file, 'rb') as f:
            current_code = f.read()
        if current_code != new_code:
            print("🔄 terdapat pembaruan script tersedia di GitHub.")
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
    # Cek yt-dlp
    print("Mengecek modul yt-dlp...")
    try:
        import yt_dlp
        print("yt-dlp sudah terinstall")
    except ImportError:
        print("yt-dlp belum terinstall. Menginstall yt-dlp...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("yt-dlp sudah terinstall")
        except Exception as e:
            print(f"Gagal install yt-dlp: {e}")
            sys.exit(1)

    # Cek ffmpeg
    print("Mengecek modul ffmpeg...")
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("ffmpeg sudah terinstall")
    except Exception:
        print("ffmpeg belum terinstall. Menginstall ffmpeg...")
        try:
            if os.name == 'nt':
                print("\nUntuk Windows, silakan download FFmpeg dari:")
                print("https://www.gyan.dev/ffmpeg/builds/")
                print("Ekstrak dan letakkan ffmpeg.exe di folder ini")
                input("Tekan Enter setelah selesai...")
            else:
                if os.system('which apt-get > /dev/null 2>&1') == 0:
                    os.system('sudo apt-get install -y ffmpeg')
                elif os.system('which yum > /dev/null 2>&1') == 0:
                    os.system('sudo yum install -y ffmpeg')
                elif os.system('which brew > /dev/null 2>&1') == 0:
                    os.system('brew install ffmpeg')
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print("ffmpeg sudah terinstall")
        except Exception as e:
            print(f"Gagal install ffmpeg: {e}")
            print("Lanjut dengan risiko beberapa fitur tidak dapat berjalan.")

# -- Jalankan urutan: update -> cek modul -- #
auto_update_script()

# Coba import yt_dlp, jika gagal akan di-handle di bawah
try:
    import yt_dlp
except ImportError:
    yt_dlp = None

def hapus_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def buat_folder_download():
    folder = "web_video_download"
    os.makedirs(folder, exist_ok=True)
    return folder

def pilih_platform():
    hapus_layar()
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
        print("Pilihan tidak valid! Silakan pilih 1-4")

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
        print("Pilihan tidak valid! Silakan pilih 1-2")

def pilih_resolusi(url):
    hapus_layar()
    print("Mengambil informasi video...")
    ydl_opts = {'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [f for f in info['formats']
                       if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            if not formats:
                print("Tidak ada format video+audio yang tersedia")
                return None, None, None
            # Jika hanya ada 1 pilihan resolusi, download otomatis
            if len(formats) == 1:
                fmt = formats[0]
                res = fmt.get('resolution', 'Unknown')
                ext = fmt.get('ext', 'Unknown')
                print(f"\nINFO: Hanya ada 1 resolusi ({res}, {ext}). Download otomatis...")
                sleep(2)
                return fmt['format_id'], res, ext
            # Jika ada beberapa pilihan, tampilkan pilihan
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
                    print("Batal memilih resolusi.")
                    return None, None, None
                try:
                    idx = int(pilihan) - 1
                    if 0 <= idx < len(formats):
                        res = formats[idx].get('resolution', 'Unknown')
                        ext = formats[idx].get('ext', 'Unknown')
                        return formats[idx]['format_id'], res, ext
                    print("Nomor tidak valid!")
                except ValueError:
                    print("Harap masukkan angka!")
    except Exception as e:
        print(f"Error: {e}")
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

def download_video(url, folder, format_id=None):
    if cek_file_sudah_ada(url, folder):
        print("\n⚠ Video sudah ada di folder download")
        return "exists"
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
            print("\n✓ Download berhasil!")
            return "success"
    except Exception as e:
        print(f"\n✗ Gagal download: {e}")
        import traceback
        traceback.print_exc()
        return "failed"

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '?')
        print(f"\rSedang download: {percent} selesai", end='', flush=True)
    elif d['status'] == 'finished':
        print("\rProses download selesai!".ljust(50))

def download_banyak_terbaik(folder, platform_domains):
    urls = []
    print("Masukkan alamat URL video satu per satu.")
    print("Jika sudah selesai, cukup tekan Enter tanpa mengetik apa-apa.")
    while True:
        url = input("Alamat = ").strip()
        if url == "":
            break
        if not any(domain in url for domain in platform_domains):
            print(f"URL tidak valid! Pastikan URL dari {', '.join(platform_domains)}")
            continue
        urls.append(url)
    if not urls:
        print("Tidak ada alamat yang dimasukkan.")
        input("Tekan Enter untuk kembali ke menu utama...")
        return
    print(f"\nMulai mendownload {len(urls)} video secara otomatis (format terbaik)...\n")
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Download: {url}")
        result = download_video(url, folder)
        if result == "success":
            print("✓ Berhasil")
        elif result == "exists":
            print("⚠ File sudah ada, download dilewati")
        else:
            print("✗ Gagal")
    print("\nSEMUA PROSES SELESAI.")
    input("Tekan Enter untuk kembali ke menu utama...")

def main():
    hapus_layar()
    cek_dan_install_modul()
    sleep(3)
    hapus_layar()
    print (" SELAMAT DATANG DI APLIKASI")
    print ("   ○ WEB VIDEO DOWNLOAD ○")
    print("-" * 40)
    sleep(4)
    folder = buat_folder_download()

    platforms = {
        '1': ['youtube.com', 'youtu.be'],
        '2': ['facebook.com', 'fb.watch'],
        '3': ['twitter.com', 'x.com']
    }

    while True:
        pilihan = pilih_platform()
        if pilihan == '4':
            print("\nTerima kasih telah menggunakan program ini!")
            break

        mode = pilih_mode_download()
        if mode == '1':
            while True:
                hapus_layar()
                url = input("Masukkan URL video: ").strip()
                if not url:
                    print("URL tidak boleh kosong!")
                    sleep(1)
                    continue
                if any(domain in url for domain in platforms[pilihan]):
                    break
                print(f"URL tidak valid! Pastikan URL dari {', '.join(platforms[pilihan])}")
                sleep(2)
            format_id = None
            res = None
            ext = None
            if pilihan in ['1', '2']:
                format_id, res, ext = pilih_resolusi(url)
                if not format_id:
                    input("Tekan Enter untuk kembali...")
                    continue
                print(f"\nDownload dimulai untuk resolusi: {res}, format: {ext}")
                sleep(1)
            hapus_layar()
            print("Memulai download...")
            result = download_video(url, folder, format_id)
            if result == "success":
                print("File tersimpan di:", os.path.abspath(folder))
            elif result == "exists":
                print("File sudah ada di folder download.")
            input("Tekan Enter untuk kembali ke menu utama...")
        else:
            hapus_layar()
            print("MODE DOWNLOAD BANYAK VIDEO")
            download_banyak_terbaik(folder, platforms[pilihan])

if __name__ == "__main__":
    main()