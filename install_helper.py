def load_dependencies():
    for dep in ["spotdl", "customtkinter", "pyyaml", "yt-dlp"]:
        try:
            import dep
        except ModuleNotFoundError:
            subprocess.run(["pip", "install", dep])
