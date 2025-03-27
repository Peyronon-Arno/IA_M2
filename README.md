Peyronon Arno Compte rendu

# 📌 Compte Rendu - Projet Playlist Generator AI

## 🎯 Contexte du Projet

Ce projet a été développé dans le cadre de l'élective du Master 2, semestre 2, en Intelligence Artificielle. L'objectif est de concevoir une application permettant de générer des playlists musicales basées sur un artiste donné, tout en fournissant une brève biographie de celui-ci grâce à une intelligence artificielle.

L'application exploite plusieurs technologies avancées pour interagir avec l'API de Spotify afin d'obtenir des morceaux pertinents et avec l'API Mistral pour générer automatiquement des descriptions textuelles de qualité.

## 🛠️ Technologies Utilisées

| Technologie    | Utilité dans le projet                                                                       |
| -------------- | -------------------------------------------------------------------------------------------- |
| **Python**     | Langage de programmation principal utilisé pour le développement                             |
| **Streamlit**  | Framework permettant de créer une interface utilisateur interactive et accessible via le web |
| **Spotipy**    | Bibliothèque Python facilitant l'interaction avec l'API Spotify                              |
| **Mistral AI** | API utilisée pour générer des descriptions d'artistes à partir de modèles d'IA avancés       |
| **dotenv**     | Gestion des variables d'environnement afin de protéger les clés API                          |

## 🚀 Première Version et Déploiement

Une première version de l'application a été développée et déployée en ligne via **Streamlit Sharing**. Après le déploiement, des tests ont été effectués en sollicitant mon entourage afin d'obtenir des retours d'expérience concrets.

## 🔍 Axes d'Amélioration Suite aux Retours Utilisateurs

Les premiers tests ont permis d'identifier plusieurs axes d'amélioration :

1. **Suppression des doublons dans la playlist** :

   - Certains morceaux apparaissaient plusieurs fois, notamment sous des formats différents (remix, live, etc.).
   - Une solution a été implémentée pour filtrer les titres de chansons de manière plus stricte.

2. **Amélioration de l'expérience utilisateur** :

   - Une interface visuelle de chargement a été ajoutée pour améliorer la fluidité de l'expérience.
   - Cela permet aux utilisateurs de mieux comprendre que le système est en train de traiter leur requête.
   - Une solution a été implémentée pour afficher un chargement des données ainsi qu'une meilleure disposition des éléments

3. **Amélioration des résultats pour les noms courts** :
   - Lors de la recherche de morceaux pour des noms d'artistes courts ou ambigus, les résultats pouvaient être trop génériques.

## 📌 Conclusion

L'itération de ce projet à travers les retours utilisateurs a permis de l'améliorer significativement. En combinant plusieurs technologies et en affinant les traitements, l'application est désormais plus robuste, plus fluide et offre une meilleure pertinence des résultats musicaux et textuels.

## URL publique

https://peyronon-arno-ia-m2-app-gdkcx0.streamlit.app/

## GIF de démonstration

![](video_rendu.gif)
