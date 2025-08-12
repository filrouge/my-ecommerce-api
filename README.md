<!-- A compléter -->
# API Flask


## Description

<!-- TODO -->
API REST développée avec Flask, SQLAlchemy et JWT.


## Structure du projet ()

my-ecommerce-api/
│
├── model/
│   └── models.py               ← modèles SQLAlchemy (contient User(), Base et Session)
│
├── routes/                     # Routes par domaine/scope
│   ├── auth_routes.py          ← contient "api/auth/register" et "api/auth/login"
│   ├── main_routes.py          ← contient "/" (home)
│   └── test_routes.py          ← contient les routes pour tests manuels
│
├── business_rules/             # Logique métier (à venir)
│
├── core/                       # Middleware sécurité
│   ├── utils.py                ← (à venir)
│   └── auth.py                 ← JWT + décorateur @auth_required (@admin_required à venir)
│
├── database/                   # (à venir)
│
├── tests/                      # Tests unitaires et intégration
│   └── test_*.py               ← fichiers pytest à venir
│
├── seed_data.py                # Scripts pour alimenter les tables (à venir, utilisant faker)
│
├── app.py                      # Point d’entrée API
│
├── .env.example                # template pour variables d'environnement (à venir)
├── .gitignore
├── requirements.txt            # liste des dépendances python (à venir)
└── README.md                   # (documentation en développement)


## Statut

✅ Réalisations :
    Routes: Register (avec password hashé) et Login (avec JWT)
    Validation des champs (email, nom, password) et unicité de l'email
    Centralisation des routes en Blueprints
    Intégration du décorateur @auth_required
    Architecture SQLAlchemy ready
    Tests ad-hoc

🔜 Reste à faire :
    Décorateur @admin_required (voire autre selon rôle)
    Modèles Produit, Commande et LignesCommande
    Logique métier (business-rules/)
    Logique SQLAlchemy à revoir (centralisée)
    Scripts seed_data.py (alimentation des tables)
    Gestion erreurs/exceptions (à généraliser/uniformiser)
	Fichiers pytest (auth + produits + commandes)	
	Variables d’environnement (credentials, config)
    Alléger le code en externalisant les fonction redondantes/querys
    Passage à Logger pour le monitoring


## Prérequis

- Python >= 3.12
- SQLite (DbBrowser)
- Conda / Virtualenv + pip


## Installation (Windows)

```bash
git clone <https://github.com/filrouge/my-ecommerce-api>
cd my-ecommerce-api
conda venv -n api_venv          # Conda
conda activate api_venv         # Conda
python -m venv api_venv         # Windows
api_venv\Scripts\activate       # Windows
pip install --upgrade pip
pip install -r requirements.txt
```


## Configuration

Configurez `.env.example` en `.env` avec vos valeurs :

```
DATABASE_URL=sqlite:///path-to-database.db
JWT_SECRET_KEY=your-jwt-secret
```

## Lancement

```bash
python app.py
```


## API Endpoints

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
