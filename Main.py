import os
import sys
import subprocess
from time import sleep

# Coba import yt_dlp, jika gagal akan di-handle di bawah
try:
    import yt_dlp
except ImportError:
    yt_dlp = None

def hapus_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def cek_dan_install_ffmpeg():
    """Memeriksa dan menginstall FFmpeg jika belum ada"""
    try:
        subprocess.run(['ffmpeg', '-version'],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL,
                      check=True)
        print("✓ FFmpeg sudah terinstall")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg tidak ditemukan, mencoba menginstall...")
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
            subprocess.run(['ffmpeg', '-version'], check=True)
            print("✓ FFmpeg berhasil diinstall!")
            return True
        except Exception as e:
            print(f"✗ Gagal menginstall FFmpeg: {e}")
            return False

def cek_dan_install_ytdlp():
    """Memeriksa dan menginstall yt-dlp jika belum ada"""
    global yt_dlp
    try:
        import yt_dlp
        print("✓ yt-dlp sudah terinstall")
        return True
    except ImportError:
        print("✗ yt-dlp tidak ditemukan, mencoba install otomatis...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            import yt_dlp as ytdlp_mod
            yt_dlp = ytdlp_mod
            print("✓ yt-dlp berhasil diinstall!")
            return True
        except Exception as e:
            print(f"✗ Gagal install yt-dlp: {e}")
            return False

def buat_folder_download():
    """Membuat folder download jika belum ada"""
    folder = "youtubedownload"
    os.makedirs(folder, exist_ok=True)
    return folder

def pilih_platform():
    """Menampilkan menu pilihan platform"""
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

def pilih_resolusi(url):
    """Menampilkan daftar resolusi yang tersedia"""
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
                return None

            print("\n╔══════════════════════════════╗")
            print("║      PILIH RESOLUSI VIDEO    ║")
            print("╠══════════════════════════════╣")
            for i, fmt in enumerate(formats):
                res = fmt.get('resolution', 'Unknown')
                ext = fmt.get('ext', 'Unknown')
                print(f"║ {i+1}. {res.ljust(8)} ({ext.ljust(5)}) ║")
            print("╚══════════════════════════════╝")

            while True:
                try:
                    pilihan = int(input("\nPilih resolusi (nomor): ")) - 1
                    if 0 <= pilihan < len(formats):
                        return formats[pilihan]['format_id']
                    print("Nomor tidak valid!")
                except ValueError:
                    print("Harap masukkan angka!")
    except Exception as e:
        print(f"Error: {e}")
        return None

def cek_file_sudah_ada(url, folder):
    """Cek apakah file sudah ada di folder"""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            nama_file = ydl.prepare_filename(info)
            path_lengkap = os.path.join(folder, os.path.basename(nama_file))
            return os.path.exists(path_lengkap)
    except:
        return False

def download_video(url, folder, format_id=None):
    """Fungsi utama untuk download video"""
    if cek_file_sudah_ada(url, folder):
        print("\n⚠ Video sudah ada di folder download")
        return True

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
            return True
    except Exception as e:
        print(f"\n✗ Gagal download: {e}")
        import traceback
        traceback.print_exc()
        return False

def progress_hook(d):
    """Progress bar satu baris sederhana"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '?')
        print(f"\rSedang download: {percent} selesai", end='', flush=True)
    elif d['status'] == 'finished':
        print("\rProses download selesai!".ljust(50))

def main():
    hapus_layar()
    print("Pastikan sudah install yt-dlp (pip install yt-dlp) dan ffmpeg.")
    print("Script akan mencoba menginstall otomatis jika belum ada.")
    print("-" * 40)
    sleep(2)

    if not cek_dan_install_ytdlp():
        input("Tekan Enter untuk keluar...")
        return

    if not cek_dan_install_ffmpeg():
        input("Tekan Enter untuk melanjutkan dengan risiko video tanpa suara...")

    folder = buat_folder_download()

    while True:
        pilihan = pilih_platform()

        if pilihan == '4':
            print("\nTerima kasih telah menggunakan program ini!")
            break

        platforms = {
            '1': ['youtube.com', 'youtu.be'],
            '2': ['facebook.com', 'fb.watch'],
            '3': ['twitter.com', 'x.com']
        }

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
        if pilihan in ['1', '2']:
            format_id = pilih_resolusi(url)
            if not format_id:
                input("Tekan Enter untuk kembali...")
                continue

        hapus_layar()
        print("Memulai download...")
        if download_video(url, folder, format_id):
            print("File tersimpan di:", os.path.abspath(folder))

        while True:
            print("\nPilihan:")
            print("1. Download video lain")
            print("2. Keluar")
            next_pilihan = input("Masukkan pilihan (1-2): ")

            if next_pilihan == '1':
                break
            elif next_pilihan == '2':
                print("\nTerima kasih telah menggunakan program ini!")
                return
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()