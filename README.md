<!-- A compléter -->
# API Flask


## Description

<!-- TODO -->
API REST construite avec les librairies **Flask**, **SQLAlchemy** et **JWT**, et qui gère les fonctionnalités suivantes :

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
│   ├── utils.py                    ← contient les logiques Authentification/Autorisation
│   └── auth.py                     ← JWT + décorateurs `@auth_required` + `@access_granted`
│
├── database/                   # (à venir)
│
├── model/                      # ORM SQLAlchemy (modèles inclus)
│   ├── database.py                 ← contient Engine & Base
│   ├── sessions.py                 ← contient Sessions
│   └── models.py                   ← contient les modèles SQLAlchemy (User, Product)
│
├── routes/                     # Routes par domaine/scope
│   ├── auth_routes.py              ← contient les routes `api/auth/register` et `api/auth/login`
│   ├── main_routes.py              ← contient `/` (home)
│   ├── order_routes.py             ← contient les routes `/api/commandes`, `/api/commandes/{id}`
│   ├── product_routes.py           ← contient les routes `/api/produits` et `/api/produits/{id}`
│   │
│   └── to_test_routes.py           ← contient les routes pour tests manuels (temporaire)
│
├── services/                   # Logique métier
│   ├── product_utils.py            ← contient les utilitaires pour les routes `produits`
│   └── order_utils.py              ← contient les utilitaires pour les routes `commandes`
│
├── tests/                      # Tests unitaires et fonctionnels
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

1. Cloner le repertoire de ce projet

```bash
git clone <https://github.com/filrouge/my-ecommerce-api>
cd my-ecommerce-api
```

2. Créer et activer l'environnement virtuel

```bash
conda venv -n api_venv          # Conda
conda activate api_venv         # Conda

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

3. Installer les dépendances

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

```bash
python app.py
```

ou bien

```bash
flask run
```

En local, l'API est disponible sur l'url : http://127.0.0.1:5000



## Tests

Pour les tests Pytest, executez les commandes suivantes directement à la racine du projet :
```bash
pytest --maxfail=1 --disable-warnings -q
```

`pytest -v` pour cibler tous les tests
`pytest -v tests/test_users.py` pour cibler un seul fichier de tests
`pytest -vv tests/test_users.py` pour afficher le détail des assertions
`pytest -v tests/test_users.py::TestLogin` pour cibler un seul module de tests
`pytest -v tests/test_users.py::TestAdminAccess::test_access_denied` pour cibler une seule fonctionnalité de tests

Pour la génération d'un rapport de tests (avec résultats dans un fichier `report.html`), il faudra installer la librairie `pytest-html` avec `pip install pytest-html` et lancer la commande :

`pytest -vv test_products.py --html=report.html --self-contained-html` 


Dans le cadre des fonctionnalités `utilisateurs` de l'API, les tests unitaires permettent de vérifier les exigences suivantes (avec gestion des erreurs) :

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



## API Endpoints

TODO: Phrase d'introduction/explication (archi, soc...)

### Authentification

| Méthode     | Endpoint                        | Description                             |
|-------------|---------------------------------|-----------------------------------------|
| **POST**    | `/api/auth/register`            | Inscription (email, password)           |
| **POST**    | `/api/auth/login`               | Connexion (avec retour de token JWT)    |


🔹 Exemple: **POST** `/api/auth/login`

        *Body*

                `{
                "email": "exemple@exemple.com",
                "password": "secret"
                }`

        *Response (200)*

                `{
                "message": "Connection succeed",
                "token": "eyJhbGciOiJIUz..."
                }`



### Produits

| Méthode     | Endpoint                        | Accès        | Description              |
|-------------|---------------------------------|--------------|--------------------------|
| **GET**     | `/api/produits`                 | Public       | Liste des produits       |
| **GET**     | `/api/produits/{id}`            | Public       | Détail produit           |
| **POST**    | `/api/produits`                 | Admin        | Création produit         |
| **PUT**     | `/api/produits/{id}`            | Admin        | Mise à jour produit      |
| **DELETE**  | `/api/produits/{id}`            | Admin        | Suppression produit      |


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

| Méthode     | Endpoint                       | Accès         | Description              |
|-------------|--------------------------------|-------------  |--------------------------|
| **GET**     | `/api/commandes`               | Client/Admin  | Liste des commandes      |
| **GET**     | `/api/commandes/{id}`          | Client/Admin  | Détail d'une commande    |
| **POST**    | `/api/commandes`               | Client        | Création d'une commande  |
| **PATCH**   | `/api/commandes/{id}`          | Admin         | Mise à jour du statut    |
| **GET**     | `/api/commandes/{id}/lignes`   | Client/Admin  | Lignes de la commande    |


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

### Erreurs applicatives

```
```


### Erreurs SQLAlchemy

```
```


## Statut

🔜 TODO:

    - Gestion et uniformisation des erreurs/exceptions (métier vs. back-end)
    - Factorisation des tests (fixtures pour produit/ligne/commande)
    - Documentation du code + Reformatage + Anglicisme
    - Enrichissement de la documentation API

    - Passage à Logger pour le monitoring (MEP)

    - Exemples + Scripts `seed_data.py` (alimentation des tables)