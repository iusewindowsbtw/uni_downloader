# https://www.youtube.com/watch?v=Miydkti_QV, padx = 10E
import yaml
import customtkinter
from yt_dlp import YoutubeDL
import subprocess
import sys  # Pour accéder au chemin de l'exécutable Python actuellement utilisé
from spotdl import __main__ as spotdl  # Pour obtenir le chemin de spotdl
import install_helper


def default_settings_write():
    print("default config!")
    data = {"outtmpl": "./output/", "format": "best"}
    try:
        with open("config/params.yml", "a+", encoding="utf-8") as params:
            yaml.dump(data, params, default_flow_style=False)
    except ImportError:
        print("could not write the params")
        pass


def settings_load() -> dict:
    try:
        with open("config/params.yml", "r+", encoding="utf-8") as params:
            data = yaml.safe_load(params)
            print(data)
            return data
    except ImportError:
        print("could not import the settings!")
        default_settings_write()
        return settings_load()


class App(customtkinter.CTk):
    def __init__(self):
        install_helper.installer()
        super().__init__()
        self.onlyaudio = False
        self.params: dict = settings_load()
        self.title("youtube downloader")
        self.geometry("400x200")
        self.resizable(False, False)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)

        self.labelframe = customtkinter.CTkFrame(master=self, fg_color="gray14")
        self.labelframe.columnconfigure(index=0, weight=1)
        self.labelframe.rowconfigure(index=0, weight=1)
        self.labelframe.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.gridframe = customtkinter.CTkFrame(master=self)
        self.gridframe.columnconfigure(index=0, weight=1)
        self.gridframe.columnconfigure(index=1, weight=1)
        self.gridframe.rowconfigure(index=0, weight=1)
        self.gridframe.rowconfigure(index=1, weight=1)
        self.gridframe.grid(row=1, column=0, columnspan=2, sticky="news")

        self.btn = customtkinter.CTkButton(
            master=self.gridframe, text="Download", command=self.downloader
        )
        self.btn.grid(row=1, column=1)

        self.input = customtkinter.CTkEntry(
            master=self.gridframe, placeholder_text="link"
        )
        self.input.grid(row=1, column=0)

        self.text = customtkinter.CTkLabel(
            master=self.labelframe, text="Universal\n downloader"
        )
        self.text.grid(row=0, column=0, columnspan=2)

        self.check = customtkinter.CTkCheckBox(
            master=self.gridframe,
            corner_radius=16,
            text="download audio\n(only for youtube)",
            command=self.set_audio,
        )
        self.check.grid(row=2, column=0, pady=20)

        self.check2 = customtkinter.CTkButton(
            master=self.gridframe,
            fg_color="gray14",
            hover_color="gray20",
            text="open config folder",
            command=self.open_explorer,
        )
        self.check2.grid(row=2, column=1, pady=20)

    def open_explorer(self, explorer_list=["thunar", "explorer"], emplacement="config"):
        for i in explorer_list:
            try:
                subprocess.run([i, emplacement])
                return
            except:
                print("trying", i, "at", emplacement)
                pass

    def downloader(self):
        input = self.input.get().strip()
        if "spotify" in input:
            subprocess.check_call([sys.executable, spotdl.__file__, input])

            # todo utiliser le module spotdl
        else:
            try:
                self.btn.configure(text="Downloading...")
                YoutubeDL(self.params).download(["ytsearch1:" + input])
                self.open_explorer(emplacement=self.params["outtmpl"])
            except:
                print("Not a valid url !")
                self.btn.configure(text="failed", fg_color="red")

    def set_audio(self):
        self.onlyaudio = not self.onlyaudio
        if self.onlyaudio:
            self.params["format"] = "bestaudio/best"
            self.params["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        else:
            self.params["format"] = "best"
            del self.params["postprocessors"]


if __name__ == "__main__":
    app = App()
    customtkinter.set_default_color_theme("config/gui.json")
    customtkinter.set_appearance_mode("dark")
    app.mainloop()
