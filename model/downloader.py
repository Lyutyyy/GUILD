import json
import subprocess
import threading
import os

class DownloadURL(object):
    def __init__(self):
        path_json_data = {}

        filename = "model/path.json"
        with open(filename, "r") as file:
            path_json_data = json.load(file)
        
        self.path_download = path_json_data['path_download']
        self.path_ytdlp = path_json_data['path_ytdlp']
        self.path_ffmpeg = path_json_data['path_ffmpeg']

    def set_music(self, url_music, quality_music, audio_format):
        self.url_music = url_music
        self.quality_music = quality_music
        self.audio_format = audio_format

    def input_json(self, choice, data):
        filename = "model/path.json"
        with open(filename, "r", encoding="utf-8") as file:
            current_data = json.load(file)

        if choice == 1:
            current_data["path_download"] = data
        elif choice == 2:
            current_data["path_ytdlp"] = data
        elif choice == 3:
            current_data["path_ffmpeg"] = data

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)

    def download(self, on_output=None):
        args = [
            self.path_ytdlp,
            "-P", self.path_download,
            f"--ffmpeg-location", self.path_ffmpeg,
            "-x",
            f"--audio-format", self.audio_format,
            f"--audio-quality", self.quality_music,
            self.url_music
        ]

        if not self.path_ytdlp or not os.path.exists(self.path_ytdlp):
            if on_output:
                on_output("Ошибка: Путь к yt-dlp не указан", "error")
            return
        
        if not self.path_download:
            if on_output:
                on_output("Ошибка: Путь установки не указан", "error")
            return
        
        if not self.path_ffmpeg or not os.path.exists(self.path_ffmpeg):
            if on_output:
                on_output("Ошибка: Путь к ffmpeg не указан", "error")
            return
        
        if not self.url_music or not self.url_music.strip():
            if on_output:
                on_output("Ошибка: URL не указан", "error")
            return

        try:
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            def read_process():
                for line in iter(process.stdout.readline, ''):
                    if on_output:
                        on_output(line, 'stdout')
                process.stdout.close()
                if on_output:
                    on_output(f"{process.returncode}", 'stdout')
            
            thread = threading.Thread(target=read_process, daemon=True)
            thread.start()

            process.wait()

        except Exception as e:
            if on_output:
                on_output(f"Ошибка: {str(e)}", "error")