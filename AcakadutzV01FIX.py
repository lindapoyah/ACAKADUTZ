import customtkinter as ctk
from tkinter import filedialog, messagebox
import webbrowser
import threading
import os
import random
import time
import subprocess
import signal
import re
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow belum terinstall. Jalankan 'pip install pillow'")
    Image = None

ctk.set_appearance_mode("light")

BG_GRAY = "#656565"
ENTRY_GRAY = "#AAAAAA"
GREEN = "#5CD02A"
GREEN_HOVER = "#388E3C"
RED = "#E61610"
RED_HOVER = "#D32F2F"
LOG_GRAY = "#A9A9A9"
PROGRESS_BG = "#656565"
PROGRESS_FILL = "#61D42A"
DONASI_YELLOW = "#FFDD00"
DONASI_RED = "#D65A66"
DONASI_ORANGE = "#F7FADE"
DONASI_FRAME_BG = "#AAAAAA"


def resource_path(relative_path):
    """Mengambil path resource yang benar baik saat dijalankan sebagai .py maupun .exe"""
    try:
        # PyInstaller membuat folder sementara di sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class VideoShufflerFree(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACAKADUTZ v1.0 - Video Shuffler & Merger - by mbombinx")
        self.geometry("950x680")
        self.resizable(False, False)
        self.configure(fg_color="white")

        # Favicon
        try:
            self.iconbitmap(resource_path("images/favicon.ico"))
            print("Favicon.ico berhasil dimuat")
        except Exception as e:
            print(f"Gagal load favicon.ico: {e}")
            try:
                icon_img = Image.open(resource_path("images/favicon.png"))
                icon = ctk.CTkImage(light_image=icon_img, size=(32, 32))
                self.wm_iconphoto(True, icon._light_image)
                print("Fallback favicon.png berhasil")
            except Exception as e2:
                print(f"Fallback favicon.png gagal: {e2}")

        self.folder_sumber = ""
        self.folder_output = ""
        self.nama_output = ctk.StringVar(value="")
        self.jumlah_video = ctk.IntVar(value=0)

        self.logo_img = self.load_logo(resource_path("images/logo.png"), (469, 100))
        self.logodev_img = self.load_logo(resource_path("images/logodev.png"), (120, 120))

        self.render_process = None
        self.is_rendering = False
        self.list_path = None
        self.output_path = None

        self.create_widgets()

    def load_logo(self, path, size):
        if Image is None:
            return None
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception as e:
            print(f"Error load logo {path}: {e}")
            return None

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="#5CD02A", height=40, corner_radius=0)
        header.pack(fill="x")
        title = ctk.CTkLabel(header, text="🎬 SOFTWARE GRATIS UNTUK MENGGABUNGKAN BEBERAPA VIDEO SECARA ACAK 🎬",
                             font=("Arial", 16, "bold"), text_color="white")
        title.pack(pady=8)

        container = ctk.CTkFrame(self, fg_color=BG_GRAY, corner_radius=8)
        container.pack(fill="both", expand=True, padx=15, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        left_column = ctk.CTkFrame(container, fg_color=BG_GRAY)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(15, 7.5), pady=10)

        logo_frame = ctk.CTkFrame(left_column, fg_color="transparent", width=469, height=100, corner_radius=8)
        logo_frame.pack(fill="x", pady=(0, 15))
        logo_frame.pack_propagate(False)
        if self.logo_img:
            ctk.CTkLabel(logo_frame, image=self.logo_img, text="").pack(expand=True)
        else:
            ctk.CTkLabel(logo_frame, text="Logo Software (file tidak ditemukan)", text_color="white").pack(expand=True)

        ctk.CTkLabel(left_column, text="Input Nama File Output:", text_color="black").pack(anchor="w", padx=20, pady=(10,0))
        entry_nama = ctk.CTkEntry(left_column, textvariable=self.nama_output, placeholder_text="Isi nama file dulu",
                                  fg_color=ENTRY_GRAY, text_color="white", width=400, height=35)
        entry_nama.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(left_column, text="Folder Sumber Video:", text_color="black").pack(anchor="w", padx=20, pady=(15,0))
        sumber_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        sumber_frame.pack(fill="x", padx=20, pady=5)
        self.entry_sumber = ctk.CTkEntry(sumber_frame, placeholder_text="Belum ada folder dipilih",
                                        fg_color=ENTRY_GRAY, text_color="white", width=300, height=35)
        self.entry_sumber.pack(side="left", fill="x", expand=True)
        btn_sumber = ctk.CTkButton(sumber_frame, text="Browse", text_color="white", fg_color=GREEN, hover_color=GREEN_HOVER,
                                   width=100, height=35, command=self.pilih_folder_sumber)
        btn_sumber.pack(side="right", padx=(10,0))

        ctk.CTkLabel(left_column, text="Folder Output:", text_color="black").pack(anchor="w", padx=20, pady=(15,0))
        output_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        output_frame.pack(fill="x", padx=20, pady=5)
        self.entry_output = ctk.CTkEntry(output_frame, placeholder_text="Belum ada folder dipilih",
                                        fg_color=ENTRY_GRAY, text_color="white", width=300, height=35)
        self.entry_output.pack(side="left", fill="x", expand=True)
        btn_output = ctk.CTkButton(output_frame, text="Browse", text_color="white", fg_color=GREEN, hover_color=GREEN_HOVER,
                                   width=100, height=35, command=self.pilih_folder_output)
        btn_output.pack(side="right", padx=(10,0))

        ctk.CTkLabel(left_column, text="Jumlah Video yang Ingin Digabung:", text_color="black").pack(anchor="w", padx=20, pady=(15,0))
        spin_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        spin_frame.pack(fill="x", padx=20, pady=5)
        entry_jumlah = ctk.CTkEntry(spin_frame, textvariable=self.jumlah_video, width=80, height=35,
                                    fg_color=ENTRY_GRAY, text_color="white")
        entry_jumlah.pack(side="left")
        ctk.CTkButton(spin_frame, text="↑", width=40, height=35, text_color="white", fg_color=GREEN, hover_color=GREEN_HOVER,
                      command=lambda: self.jumlah_video.set(self.jumlah_video.get() + 1)).pack(side="left", padx=5)
        ctk.CTkButton(spin_frame, text="↓", width=40, height=35, text_color="white", fg_color=GREEN, hover_color=GREEN_HOVER,
                      command=lambda: self.jumlah_video.set(max(0, self.jumlah_video.get() - 1))).pack(side="left")

        btn_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        btn_frame.pack(pady=30)
        self.btn_proses = ctk.CTkButton(btn_frame, text="Proses", fg_color=GREEN, hover_color=GREEN_HOVER, width=180, height=50,
                                        font=("Arial", 16, "bold"), command=self.start_render)
        self.btn_proses.pack(side="left", padx=40)

        self.btn_batal = ctk.CTkButton(btn_frame, text="Batalkan", fg_color=RED, hover_color=RED_HOVER, width=180, height=50,
                                       font=("Arial", 16, "bold"), command=self.cancel_render)
        self.btn_batal.pack(side="left", padx=40)

        right_column = ctk.CTkFrame(container, fg_color=LOG_GRAY, corner_radius=8)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(7.5, 15), pady=10)

        log_container = ctk.CTkFrame(right_column, fg_color=LOG_GRAY, corner_radius=8, border_width=2, border_color="#444444")
        log_container.pack(fill="both", expand=True, padx=10, pady=(10, 20))

        ctk.CTkLabel(log_container, text="Log Aktivitas:", text_color="white", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(10,5))

        self.log_box = ctk.CTkTextbox(log_container, fg_color="#c0c0c0", text_color="black", height=220, font=("Arial", 12))
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0,10))
        self.log_box.insert("end", "Siap render..\n")
        self.log_box.configure(state="disabled")

        progress_frame = ctk.CTkFrame(log_container, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15, pady=(0,10))

        self.percent_label = ctk.CTkLabel(progress_frame, text="0%", font=("Arial", 13, "bold"), text_color="black")
        self.percent_label.pack(anchor="center", pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=350, height=20, progress_color=PROGRESS_FILL, fg_color=PROGRESS_BG)
        self.progress_bar.pack(anchor="center")
        self.progress_bar.set(0)

        # Loading indicator
        loading_frame = ctk.CTkFrame(log_container, fg_color="transparent")
        loading_frame.pack(fill="x", padx=15, pady=(10, 0))

        self.loading_label = ctk.CTkLabel(loading_frame, text="Memproses...", font=("Arial", 12, "bold"), text_color="white")
        self.loading_label.pack(anchor="center")

        self.loading_bar = ctk.CTkProgressBar(loading_frame, mode="indeterminate", width=350, height=15, progress_color=GREEN)
        self.loading_bar.pack(anchor="center", pady=5)
        self.loading_bar.pack_forget()  # Sembunyikan dulu

        donasi_container = ctk.CTkFrame(right_column, fg_color=DONASI_FRAME_BG, corner_radius=8, border_width=2, border_color="#444444")
        donasi_container.pack(fill="x", padx=10, pady=(0, 10))

        donasi_inner = ctk.CTkFrame(donasi_container, fg_color="transparent")
        donasi_inner.pack(fill="both", expand=True, padx=20, pady=15)
        donasi_inner.grid_columnconfigure(0, weight=1)
        donasi_inner.grid_columnconfigure(1, weight=1)

        logo_dev_frame = ctk.CTkFrame(donasi_inner, fg_color="transparent", width=150, height=150, corner_radius=0)
        logo_dev_frame.grid(row=0, column=0, sticky="ns", padx=(0, 30), pady=10)
        logo_dev_frame.pack_propagate(False)
        if self.logodev_img:
            ctk.CTkLabel(logo_dev_frame, image=self.logodev_img, text="").pack(expand=True)
        else:
            ctk.CTkLabel(logo_dev_frame, text="Logo Developer", text_color="white").pack(expand=True)

        btn_column = ctk.CTkFrame(donasi_inner, fg_color="transparent")
        btn_column.grid(row=0, column=1, sticky="ns")
        btn_column.pack_propagate(False)

        ctk.CTkButton(btn_column, text="☕ Buy me a coffee", text_color="black", fg_color="#FFDD00", hover_color="#FFD633", width=250, height=50,
                      font=("Arial", 11), corner_radius=25, command=lambda: webbrowser.open("https://buymeacoffee.com/mbombink")).pack(anchor="center", pady=12)

        ctk.CTkButton(btn_column, text="☕ Trakteer Kopi Dong", text_color="white", fg_color="#be1e2d", hover_color="#a51825", width=250, height=50,
                      font=("Arial", 11), corner_radius=25, command=lambda: webbrowser.open("https://trakteer.id/mbombink")).pack(anchor="center", pady=12)

        ctk.CTkButton(btn_column, text="Follow Me!", text_color="black", fg_color="#F7FADE", hover_color="#DADDBD", width=250, height=50,
                      font=("Arial", 11), corner_radius=25, command=lambda: webbrowser.open("https://instagram.com/mbombinx")).pack(anchor="center", pady=12)

    def show_loading(self):
        self.loading_label.configure(text="Memproses...")
        self.loading_bar.start()
        self.loading_bar.pack(anchor="center", pady=5)
        self.update_idletasks()

    def hide_loading(self):
        self.loading_bar.stop()
        self.loading_bar.pack_forget()
        self.update_idletasks()

    def log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def pilih_folder_sumber(self):
        folder = filedialog.askdirectory(title="Pilih Folder Sumber Video")
        if folder:
            self.folder_sumber = folder
            self.entry_sumber.delete(0, "end")
            self.entry_sumber.insert(0, folder)
            self.log(f"Folder sumber dipilih: {folder}")
            videos = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
            jumlah = len(videos)
            self.log(f"Jumlah video terdeteksi: {jumlah}")

    def pilih_folder_output(self):
        folder = filedialog.askdirectory(title="Pilih Folder Output")
        if folder:
            self.folder_output = folder
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, folder)
            self.log(f"Folder output dipilih: {folder}")

    def cancel_render(self):
        if self.is_rendering:
            self.log("Proses render dibatalkan oleh user...")
            messagebox.showinfo("Dibatalkan", "Proses render dibatalkan")

            if self.render_process and self.render_process.poll() is None:
                try:
                    self.render_process.send_signal(signal.CTRL_C_EVENT if os.name == 'nt' else signal.SIGINT)
                    time.sleep(0.5)
                except Exception as kill_err:
                    self.log(f"Error kill process: {kill_err}")

            self.render_process = None
            self.is_rendering = False
            self.progress_bar.set(0)
            self.percent_label.configure(text="0%")
            self.hide_loading()
            self.btn_proses.configure(state="normal")
            self.btn_batal.configure(fg_color=RED, hover_color=RED_HOVER)

            if self.output_path and os.path.exists(self.output_path):
                try:
                    os.remove(self.output_path)
                    self.log(f"File output sementara dihapus karena dibatalkan: {self.output_path}")
                except Exception as rm_err:
                    self.log(f"Gagal hapus file output: {rm_err}")

            if self.list_path and os.path.exists(self.list_path):
                try:
                    os.remove(self.list_path)
                except:
                    pass
            self.list_path = None
            self.output_path = None

    def start_render(self):
        if self.is_rendering:
            messagebox.showinfo("Info", "Proses render sedang berjalan.")
            return
        threading.Thread(target=self.proses_render, daemon=True).start()

    def get_total_duration(self, videos):
        total = 0
        ffprobe_path = resource_path("binaries/ffprobe.exe")
        for video in videos:
            path = os.path.join(self.folder_sumber, video)
            cmd = [
                ffprobe_path, "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", path
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                duration = float(result.stdout.strip())
                total += duration
            except:
                pass
        return total

    def proses_render(self):
        self.is_rendering = True
        self.btn_proses.configure(state="disabled")
        self.btn_batal.configure(fg_color="#B71C1C", hover_color="#9A0007")
        self.show_loading()
        self.list_path = None
        self.output_path = None

        try:
            jumlah = self.jumlah_video.get()
            if jumlah <= 0:
                messagebox.showwarning("Input Salah", "Masukkan jumlah video yang valid!")
                return

            if not self.folder_sumber:
                messagebox.showwarning("Error", "Pilih folder sumber video dulu!")
                return

            if not self.folder_output:
                messagebox.showwarning("Error", "Pilih folder output dulu!")
                return

            nama_file = self.nama_output.get().strip()
            if not nama_file:
                messagebox.showwarning("Error", "Masukkan nama file output!")
                return

            if not nama_file.lower().endswith('.mp4'):
                nama_file += '.mp4'

            self.output_path = os.path.join(self.folder_output, nama_file)

            videos = [f for f in os.listdir(self.folder_sumber) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
            if len(videos) < jumlah:
                messagebox.showerror("Error", f"Hanya ada {len(videos)} video di folder! Butuh {jumlah}.")
                return

            total_videos = len(videos)
            self.log(f"Memulai memilih video yang akan dirender...")
            self.progress_bar.set(0)
            self.percent_label.configure(text="0%")

            random.shuffle(videos)
            selected_videos = videos[:jumlah]

            self.log("Membuat daftar file untuk render...")
            self.list_path = os.path.join(self.folder_output, "temp_file_list.txt")
            with open(self.list_path, "w", encoding="utf-8") as f:
                for video in selected_videos:
                    full_path = os.path.join(self.folder_sumber, video).replace('\\', '/')
                    f.write(f"file '{full_path}'\n")

            self.log("Menghitung total durasi video...")
            total_duration = self.get_total_duration(selected_videos)
            self.log(f"Total durasi video yang akan dirender: {total_duration:.2f} detik")

            self.hide_loading()
            self.log("Proses render video dimulai...")

            ffmpeg_path = resource_path("binaries/ffmpeg.exe")
            cmd = [
                ffmpeg_path, "-f", "concat", "-safe", "0",
                "-i", self.list_path,
                "-c", "copy", "-y",
                "-progress", "pipe:1", "-nostats", self.output_path
            ]

            creationflags = 0
            if os.name == 'nt':
                creationflags = subprocess.CREATE_NO_WINDOW  # Hilangkan CMD pop-up

            self.render_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1,
                universal_newlines=True,
                creationflags=creationflags
            )

            current_time = 0

            for line in iter(self.render_process.stdout.readline, ''):
                if not self.is_rendering:
                    break

                line = line.strip()
                if "out_time_ms=" in line:
                    match = re.search(r"out_time_ms=(\d+)", line)
                    if match:
                        ms = int(match.group(1))
                        current_time = ms / 1000000.0
                        if total_duration > 0:
                            percent = min(100, int((current_time / total_duration) * 100))
                            self.progress_bar.set(percent / 100)
                            self.percent_label.configure(text=f"{percent}%")
                            self.log(f"Rendering: {percent}%")
                            self.update_idletasks()

            if self.is_rendering and self.render_process and self.render_process.poll() is None:
                try:
                    self.render_process.wait()
                except Exception as wait_err:
                    self.log(f"Error wait process: {wait_err}")

            if not self.is_rendering:
                self.log("Proses dibatalkan oleh user.")
                return

            self.progress_bar.set(1)
            self.percent_label.configure(text="100%")

            if self.render_process and self.render_process.returncode == 0:
                self.log(f"Proses render {jumlah} video dari {total_videos} video secara acak telah selesai!")
                messagebox.showinfo("Sukses", f"Proses render {jumlah} video dari {total_videos} video secara acak telah selesai!\nFile: {nama_file}\nLokasi: {self.folder_output}")
            else:
                self.log("Proses dibatalkan oleh User")

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")

        finally:
            self.hide_loading()
            if self.list_path and os.path.exists(self.list_path):
                try:
                    os.remove(self.list_path)
                except:
                    pass
            self.list_path = None

            if self.output_path and os.path.exists(self.output_path):
                if not self.is_rendering:
                    try:
                        os.remove(self.output_path)
                        self.log(f"File output dihapus karena dibatalkan: {self.output_path}")
                    except:
                        pass

            self.output_path = None
            self.render_process = None
            self.is_rendering = False
            self.btn_proses.configure(state="normal")
            self.btn_batal.configure(fg_color=RED, hover_color=RED_HOVER)

if __name__ == "__main__":
    app = VideoShufflerFree()
    app.mainloop()
