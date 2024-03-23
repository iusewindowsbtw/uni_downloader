import subprocess

# L'URL de Spotify que vous souhaitez télécharger
spotify_url = "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"

# Exécutez SpotDL avec l'URL de Spotify comme argument
subprocess.run(["spotdl", spotify_url])

