<!-- A compléter -->
# API Flask


## Description

<!-- TODO -->
**API REST** construite avec les librairies **Flask**, **SQLAlchemy** et **JWT**, et qui gère les fonctionnalités suivantes :

- Authentification des utilisateurs :
    - Inscription (register)
    - Connexion (login + JWT)

- Gestion des produits (CRUD selon permissions)
    - navigation / affichage / recherche
    - ajout / modification / suppression (admin)

- Gestion des commandes :
    - création / ajout / consultation
    - consultation / suivi / modification



## Structure du projet

TODO: Phrase d'introduction/explication (archi, soc...)

```
my-ecommerce-api/
│
├── app.py                      # Point d’entrée API (+ Blueprints)
├── config.py                   # Paramêtres de configuration Flask/SQLAlchemy
│
├── core/                       # Middleware sécurité
│   ├── __init__.py                 ← 
│   ├── auth_utils.py               ← contient les logiques Authentification/Autorisation
│   └── auth.py                     ← JWT + décorateurs (`@auth_required`, `@access_granted`)
│
├── database/                   # (à venir)
│
├── model/                      # ORM SQLAlchemy
│   ├── __init__.py                 ← 
│   ├── database.py                 ← contient Engine & Base
│   ├── sessions.py                 ← contient Sessions + Handler des erreurs SQLAlchemy
│   └── models.py                   ← contient les modèles SQLAlchemy (User, Product)
│
├── routes/                     # Routes par domaine/scope
│   ├── __init__.py                 ← 
│   ├── auth_routes.py              ← contient les routes `api/auth/register` et `api/auth/login`
│   ├── main_routes.py              ← contient `/` (home)
│   ├── order_routes.py             ← contient les routes `/api/commandes`, `/api/commandes/{id}`
│   ├── product_routes.py           ← contient les routes `/api/produits` et `/api/produits/{id}`
│   │
│   └── to_test_routes.py           ← contient les routes pour tests manuels (temporaire)
│
├── services/                   # Logique métier
│   ├── __init__.py                 ← 
│   ├── product_utils.py            ← contient les utilitaires pour les routes `produits`
│   └── order_utils.py              ← contient les utilitaires pour les routes `commandes`
│
├── tests/                      # Tests unitaires et fonctionnels
│   ├── __init__.py                 ← 
│   ├── conftest.py                 ← fichier de configuration/centralisation des fixtures (en développement)
│   ├── report.html                 ← rapport des résultats de tests pytest (HTML) (optionnel)
│   ├── test_users.py               ← fichier pytest pour `User`
│   ├── test_products.py            ← fichier pytest pour `Product`
│   └── test_orders.py              ← fichier pytest pour `Order`
│
├── options/                    # Pour simulation API / BdD (optionnel)
│   └── seed_data.py                ← Scripts pour alimenter les tables (à venir / optionnel)
│
├── .gitignore
├── requirements.txt            # Liste des dépendances python (à venir)
└── README.md                   # (documentation en développement)
```


## Prérequis

L'implémentation du code nécessite les conditions suivantes :

    - Python >= 3.12
    - conda / virtualenv + pip

L'utilisation de l'outil SQLite (DB Browser) est optionnelle.
Elle permet néanmoins de vérifier :

    - le schéma de la Base,
    - la création des tables, et 
    - les données enregistrées, modifiées ou supprimées.


## Installation (Conda, Linux/Windows)

TODO: Phrase d'introduction/explication (archi, soc...)

1. Clonez le repertoire de ce projet

```bash
git clone https://github.com/filrouge/my-ecommerce-api.git
cd my-ecommerce-api
```

2. Créez et activez l'environnement virtuel

```bash
conda venv -n api_venv          # Conda
conda activate api_venv         # Conda

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

3. Installez les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```



## Configuration

Une fois le projet cloné et l'environnement crée, modifiez le fichier `config.py` avec vos propres valeurs :

```
DATABASE_URL=sqlite:///path-to-database.db
JWT_SECRET_KEY=your-jwt-secret
```


## Lancement

Pour lancer l'application, tapez `python app.py` à la racine du projet; l'option `--debug` permet d'activer le mode *DEBUG*.
La ommande `flask run --debug` permet également une utilisation locale de l'application en mode debug
L'API sera disponible sur l'url http://127.0.0.1:5000.

<!-- ![alt text](image.png) -->



## API Endpoints

TODO: Phrase d'introduction/explication (archi, soc...)
<!-- 
- **200 OK** : succès (action GET/PUT/DELETE ou PATCH)
- **201 Created** : ressource créée (POST)
 -->


### Authentification

| Méthode     | Endpoint                       | Description                           |
|-------------|--------------------------------|---------------------------------------|
| **POST**    | `/api/auth/register`           | Inscription (email, password)         |
| **POST**    | `/api/auth/login`              | Connexion (avec retour de token JWT)  |


🔹 Exemple: **POST** `/api/auth/login`

*Body*
```
    {
    "email": "exemple@exemple.com",
    "password": "secret"
    }

```

*Response (200)*
```
    {
    "message": "Connection succeed",
    "token": "eyJhbGciOiJIUz..."
    }
```


### Produits

| Méthode     | Endpoint                       | Accès        | Description                                 |
|-------------|--------------------------------|--------------|---------------------------------------------|
| **GET**     | `/api/produits`                | Public       | Liste tous les produits                     |
| **GET**     | `/api/produits/{id}`           | Public       | Détail d'un produit spécifique              |
| **POST**    | `/api/produits`                | Admin        | Création de produit dans le catalogue       |
| **PUT**     | `/api/produits/{id}`           | Admin        | Mise à jour des caractéristiques de produit |
| **DELETE**  | `/api/produits/{id}`           | Admin        | Suppression d'un produit spécifique         |


🔹 Exemple: **POST** `/api/produits`    (*headers:* `Authorization: Bearer <token_admin>`)

*Body*
    `{
    "nom": "Produit",
    "prix": 99.9,
    "stock": 5
    }`

*Response (201)*
    `{
    "message": "Produit ajouté",
    "produit": {
        "id": 3,
        "nom": "Produit",
        "prix": 99.9,
        "stock": 5
    }
    }`


### Commandes

| Méthode     | Endpoint                      | Accès         | Description                                 |
|-------------|-------------------------------|---------------|---------------------------------------------|
| **GET**     | `/api/commandes`              | Client/Admin  | Liste toutes les commandes admin ou client  |
| **GET**     | `/api/commandes/{id}`         | Client/Admin  | Détails d'une commande spécifique           |
| **POST**    | `/api/commandes`              | Client        | Création de commandes                       |
| **PATCH**   | `/api/commandes/{id}`         | Admin         | Mise à jour du statut de la commande        |
| **GET**     | `/api/commandes/{id}/lignes`  | Client/Admin  | Liste les lignes d'une commande spécifique  |


🔹 Exemple: **POST** `/api/commandes`   (*headers:* `Authorization: Bearer <token_client>`)

*Body*
    `{
    "adresse_livraison": "4 rue d'ici, 75000 Paname",
    "produits": [
        {"id": 1, "quantite": 2},
        {"id": 2, "quantite": 1}
    ]
    }`

*Response (201)*
    `{
    "message": "Commande id:11 créée",
    "commande": {
        "id": 11,
        "statut": "En attente",
        "adresse_livraison": "4 rue d'ici, 75000 Paname",
        "produits": [
        {"id": 1, "quantite": 2},
        {"id": 2, "quantite": 1}
        ]
    }
    }`



## Gestion des erreurs/exceptions

Les erreurs applicatives (métier) et SQLAlchemy (back-end) sont gérées de manière disctincte pour une meilleure séparation des responsabilités.
Elles sont renvoyées sous forme de messages explicitant la cause, via `jsonify({"error": ...})` et incluant les codes HTTP suivants: 

- **400 Bad Request** : données manquantes/invalidées (validation payload/body)
- **401 Unauthorized** : authentification manquante ou JWT invalide/absent.
- **403 Forbidden** : accès non autorisé (restriction POST/PUT/DELETE ou PATCH)
- **404 Not Found** : ressource absente ou inexistante


### Erreurs applicatives

<!--
Authentification :

Autorisation :

Produits :

Commandes :

Autres

-->


### Erreurs SQLAlchemy

Les erreurs SQLAlchemy sont sous la forme générique `500 Internal Server Error`.
Ces erreurs (et leurs causes) sont gérées de manière centralisée par un `errorhandler` qui fournit des *messages de sortie personnalisés* (non décrits ici) sous la forme : `{"error": "DataBase - <message>"}, <code>` :

| Exception                |     Code     |                       Cause                         |
|--------------------------|--------------|-----------------------------------------------------|
| **IntegrityError**       |     `409`    |     Violation de contraintes (unique, null, fk …)   |
| **OperationalError**     |     `503`    |     Problème côté DataBase (connexion, timeout…)    |
| **DataError**            |     `400`    |     Type/Format de données invalide                 |
| **StatementError**       |     `500`    |     Erreur dans l’exécution SQL                     |
| **autres**               |     `500`    |     Erreur interne inconnue                         |



## Tests

Pour lancer les tests Pytest, executez les commandes suivantes directement à la racine du projet (avec l'option `--maxfail=1 --disable-warnings` si besoin) :

`pytest -v` pour cibler tous les tests
`pytest -v tests/test_users.py` pour cibler un seul fichier de tests
`pytest -vv tests/test_users.py` pour afficher le détail des assertions
`pytest -v tests/test_users.py::TestLogin` pour cibler un seul module de tests
`pytest -v tests/test_users.py::TestAdminAccess::test_access_denied` pour cibler une seule fonctionnalité de tests


*Optionel*: Pour générer un rapport d'exécution des tests, installez la librairie `pytest-html` avec `pip install pytest-html`, lancez la commande suivante puis ouvrez le fichier `mon-rapport-pytest.html`:

    ```pytest -vv test_products.py --html=mon-rapport-pytest.html --self-contained-html``` 


Dans le cadre des fonctionnalités de l'API, ces tests unitaires permettent de vérifier les exigences (`utilisateurs`) suivantes :

~ Inscription (`/api/auth/register`)
    - email unique
    - mot de passe haché
    - rôle (défaut = client)

~ Connexion (`/api/auth/login`)
    - validée avec token JWT renvoyé
    - refusée si mauvais mot de passe

~ Accès restreint (`/api/admin-only-route`)
    - autorisé pour `admin`
    - refusé pour autre que `admin`


TODO: Compléter la couverture des test pour `produits` et `commandes`



## Statut

🔜 TODO:

    - Gestion et uniformisation des erreurs/exceptions (métier vs. back-end)
    - Factorisation des tests (fixtures pour produit/ligne/commande)
    - Documentation du code + Reformatage + Anglicisme
    - Enrichissement de la documentation API

    - Passage à Logger pour le monitoring (MEP)

    - Exemples + Scripts `seed_data.py` (alimentation des tables)