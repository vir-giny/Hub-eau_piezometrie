# Hub-eau : Piézométrie autour de Valence

Récupération et analyse des niveaux des nappes phréatiques (piézométrie)
dans un rayon de 50 km autour de Valence (Drôme), à partir de l'API publique Hub'Eau.

## Source des données

- [API Hub'Eau – Piézométrie](https://hubeau.eaufrance.fr/page/api-piezometrie)
- API publique, sans authentification

## Structure du projet

    Hub-eau/
    ├── notebooks/        # notebooks d'exploration et d'analyse
    ├── src/              # fonctions réutilisables (appels API, pagination)
    ├── data/
    │   ├── raw/          # données brutes de l'API (non versionnées)
    │   └── processed/    # données nettoyées
    ├── .env.example      # modèle des variables d'environnement
    └── requirements.txt  # dépendances Python

## Installation

    git clone git@github.com:vir-giny/Hub-eau.git
    cd Hub-eau
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

## Utilisation

Ouvrir le notebook dans VS Code et sélectionner le kernel `.venv`.

## Statut

🚧 En cours : connexion à l'API et récupération des stations.
