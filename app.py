import spotipy
import openai
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
import os
from mistralai import Mistral

model = "mistral-large-latest"


os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Authentification avec les clés API Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="af7be259471e4fd6b88db02493dfb31d",
        client_secret="48341028f0fa4b94afa0f1b1b8eb3bcf",
    )
)


client = Mistral(api_key="Jbr2xIzpacA6GfH29M6bFSBHoIfhHsBo")


# Fonction pour générer une playlist
def get_playlist(prompt):
    results = sp.search(q=f"{prompt}", type="track", limit=15)
    tracks = []
    for track in results["tracks"]["items"]:
        track_info = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
        }
        tracks.append(track_info)
    return tracks


def generate_description(artist_name):
    chat_response = client.chat.complete(
        model=model,
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
    "Entrez le nom d'un artiste et obtenez une playlist adaptée, accompagnée d'une description générée par l'IA!"
)

prompt = st.text_input("Entrez un artiste ", "")

if st.button("Générer ma playlist"):
    if prompt:
        # Générer la playlist basée sur l'ambiance
        playlist = get_playlist(prompt)

        # Afficher la playlist générée
        st.write(f"🎶 Playlist pour **{prompt}** :")
        for track in playlist:
            st.markdown(f"- [{track['name']} - {track['artist']}]({track['url']})")

        # Générer une description via l'IA
        description = generate_description(prompt)
        st.write(f"🌟Description de l'artiste {prompt} :")
        st.write(description)
    else:
        st.warning("Entrez un prompt pour générer une playlist !")
