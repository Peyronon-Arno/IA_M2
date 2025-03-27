import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API depuis les variables d'environnement
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")  # Valeur par défaut

print("SPOTIFY_CLIENT_ID:", os.getenv("SPOTIFY_CLIENT_ID"))  # Debug
print("SPOTIFY_CLIENT_SECRET:", os.getenv("SPOTIFY_CLIENT_SECRET"))  # Debug

os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Authentification avec les clés API Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
)

# Initialisation du client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)


# Fonction pour générer une playlist avec suppression des doublons basés sur le titre
def get_playlist(prompt, target_size=15):
    unique_tracks = {}  # Stocker les morceaux uniques (clé = titre)
    limit = 15  # Nombre de morceaux récupérés par requête
    offset = 0  # Décalage pour récupérer plus de morceaux si besoin

    while len(unique_tracks) < target_size:
        results = sp.search(q=prompt, type="track", limit=limit, offset=offset)
        tracks = results.get("tracks", {}).get("items", [])

        for track in tracks:
            track_title = track["name"].strip().lower()  # Normalisation du titre

            if track_title not in unique_tracks:  # Vérifie si le titre est déjà ajouté
                unique_tracks[track_title] = {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "url": track["external_urls"]["spotify"],
                }

            # Stop si on a assez de morceaux uniques
            if len(unique_tracks) >= target_size:
                break

        # Augmenter l'offset pour récupérer plus de morceaux si besoin
        offset += limit

        # Si plus de morceaux trouvés dans l'API et on n'a pas atteint target_size, on s'arrête
        if not tracks:
            break

    return list(unique_tracks.values())


# Fonction pour générer une biographie de l'artiste
def generate_description(artist_name):
    chat_response = client.chat.complete(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in music.",
            },
            {
                "role": "user",
                "content": f"Fournis une brève biographie de l'artiste {artist_name}.",
            },
        ],
    )

    return chat_response.choices[0].message.content


# Interface Streamlit
st.title("🎵 Playlist Generator AI")
st.write(
    "Entrez le nom d'un artiste et obtenez une playlist et une description générée par l'IA!"
)

# Agencement en ligne (input + bouton)
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_input("Entrez un artiste", "")

with col2:
    st.markdown(
        """
        <style>
            div.stButton > button {
                width: 100%;
                color: black;
                border-color: white;
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            
        </style>
        """,
        unsafe_allow_html=True,
    )
    generate = st.button("🔍 Générer")

if generate and prompt:
    # Affichage du message de chargement
    with st.spinner(f"✨ Génération de la description de **{prompt}** en cours..."):
        description = generate_description(prompt)

    # Afficher la description en premier
    st.subheader(f"🌟 Description de {prompt} :")
    st.write(description)

    # Générer la playlist avec suppression des doublons et complétion
    playlist = get_playlist(prompt)

    if playlist:
        st.subheader(f"🎶 Playlist pour {prompt} :")

        # Affichage en deux colonnes
        col1, col2 = st.columns(2)
        for i, track in enumerate(playlist):
            track_info = f"- [{track['name']} - {track['artist']}]({track['url']})"
            if i % 2 == 0:
                col1.markdown(track_info)
            else:
                col2.markdown(track_info)
    else:
        st.warning("Aucun morceau trouvé pour cet artiste.")
elif generate and not prompt:
    st.warning("Entrez un artiste pour générer une playlist !")
