<!-- A compléter -->
# API Flask


## Description

<!-- TODO -->
API REST développée avec Flask, SQLAlchemy et JWT.


## Structure du code

TODO: Phrase d'introduction/explication (archi, soc...)

<pre> ```
plaintext
my-ecommerce-api/
│
├── app.py                      # Point d’entrée API
├── config.py                   # Paramêtres de configuration Flask/SQLAlchemy
│
├── business_rules/             # Logique métier (à venir)
│
├── core/                       # Middleware sécurité
│   ├── utils.py                ← (à venir)
│   └── auth.py                 ← JWT + décorateur @auth_required (@admin_required à venir)
│
├── database/                   # (à venir)
│
├── model/
│   ├── database.py             ← contient Engine & Base
│   ├── sessions.py             ← contient Sessions
│   └── models.py               ← modèles SQLAlchemy (contient User())
│
├── routes/                     # Routes par domaine/scope
│   ├── auth_routes.py          ← contient "api/auth/register" et "api/auth/login"
│   ├── main_routes.py          ← contient "/" (home)
│   │
│   ├── order_routes.py         ← (à venir: routes commande/ligne de commande)
│   ├── product_routes.py       ← (à venir: routes dédiées produits)
│   │
│   └── test_routes.py          ← contient les routes pour tests manuels
│
├── tests/                      # Tests unitaires et intégration
│   └── test_*.py               ← fichiers pytest à venir
│
├── options/                    # Dossier de simulation API / BdD
│   └── seed_data.py            ← Scripts pour alimenter les tables (à venir)
│
├── .env.example                # (à voire - redondance avec config.py)
├── .gitignore
├── requirements.txt            # Liste des dépendances python (à venir)
└── README.md                   # (documentation en développement)
``` </pre>



## Statut

### ✅ Réalisations :
    - Routes: `Register` (avec password hashé) et `Login` (avec token JWT)
    - Validation des champs (email, nom, password) et unicité de l'email
    - Centralisation des routes en Blueprints
    - Intégration du décorateur `@auth_required`
    - Architecture SQLAlchemy ready
    - Logique database/session centralisée
    - Configuration (`config.py`)
    - Tests ad-hoc

### 🔜 Reste à faire :
    - Décorateur `@admin_required` (voire autre selon rôle)
    - Modèles **Produit**, **Commande** et **LignesCommande**
    - Logique métier (business-rules/)
    - Scripts `seed_data.py` (alimentation des tables)
    - Gestion erreurs/exceptions (à généraliser/uniformiser)
    - Fichiers `pytest` (auth + produits + commandes)	
    - Variables d’environnement (credentials)
    - Alléger le code en externalisant les fonctions/querys
    - Passage à Logger pour le monitoring (MEP)



## Prérequis

L'implémentation du code nécessite les conditions suivantes
    - Python >= 3.12
    - conda / virtualenv + pip

L'utilisation de l'outil SQLite (DbBrowser) est optionnelle.
Elle permet néanmoins de vérifier :
    - le schéma de la Base,
    - la création des tables, et 
    - les données enregistrées, modifiées ou supprimées.


## Installation (Windows)

TODO: Phrase d'introduction/explication (archi, soc...)

1. Cloner le repertoire de ce projet

```bash
git clone <https://github.com/filrouge/my-ecommerce-api>
cd my-ecommerce-api
```

2. Créer et activer l'environnement virtuel

```bash
conda venv -n api_venv          # Conda
conda activate api_venv         # Conda

python -m venv api_venv         # Windows
api_venv\Scripts\activate       # Windows
```

3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## Configuration

Une fois le repo cloné et l'environnement crée, modifiez le fichier `config.py` avec vos propres valeurs :

```
DATABASE_URL=sqlite:///path-to-database.db
JWT_SECRET_KEY=your-jwt-secret
```



## Lancement

```bash
python app.py
```



## API Endpoints

TODO: Phrase d'introduction/explication (archi, soc...)

### Authentification

| Méthode | Endpoint                      | Description                             |
|---------|-------------------------------|-----------------------------------------|
| POST    | /api/auth/register            | Inscription (email, password)           |
| POST    | /api/auth/login               | Connexion (avec retour de token JWT)    |



### Produits

| Méthode | Endpoint                      | Accès        | Description              |
|---------|-------------------------------|--------------|--------------------------|
| GET     | /api/produits                 | Public       | Liste des produits       |
| GET     | /api/produits/{id}            | Public       | Détail produit           |
| POST    | /api/produits                 | Admin        | Création produit         |
| PUT     | /api/produits/{id}            | Admin        | Mise à jour produit      |
| DELETE  | /api/produits/{id}            | Admin        | Suppression produit      |



### Commandes

| Méthode | Endpoint                     | Accès         | Description              |
|---------|------------------------------|-------------  |--------------------------|
| GET     | /api/commandes               | Client/Admin  | Liste des commandes      |
| GET     | /api/commandes/{id}          | Client/Admin  | Détail d'une commande    |
| POST    | /api/commandes               | Client        | Création d'une commande  |
| PATCH   | /api/commandes/{id}          | Admin         | Mise à jour du statut    |
| GET     | /api/commandes/{id}/lignes   | Client/Admin  | Lignes de la commande    |



## Essai
<!-- TODO -->


## Tests
<!-- TODO -->