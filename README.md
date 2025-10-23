<!-- A compléter -->
# API Flask

## 📑 Table des matières
- 📌 [Description](#-description)  

- 📂 [Structure du projet](#-structure-du-projet)  
    - ⚙️ [Prérequis](#️-prérequis)
    - 🚀 [Installation](#-installation)
    - 🔧 [Configuration](#-configuration)
    - ▶️ [Lancement](#️-lancement)  

- 📄 [Documentation API](#-documentation-api)  

- 🧪 [Tests](#-tests)  

- 📌 [TODO](#-todo)  

---

## 📌 Description

**API REST** construite avec **Flask**, **SQLAlchemy**, **JWT** et **Pydantic**.  

Fonctionnalités principales :

- 👤 *Gestion des utilisateurs*  
- 📦 *Gestion des produits*  
- 🛒 *Gestion des commandes*  
  
<br>

Architecture modulaire avec séparation des responsabilités :

- logique HTTP (request/response, status code): `routes/`
- logique métier et manipulation de la base (g.session): `services/`
- centralisation des entités/relations SQLAlchemy: `model/`
- socle d'infrastructure commun (connexion, JWT, sécurité): `core/`
- validation et typage automatique (Pydantic): `schemas/`


![Architecture](docs/img/architecture.png)


<br>

> 📂 Consultez [api_endpoints.md](docs/api_endpoints.md) pour plus d’informations sur l'architecture et les fonctionnalités de l'API.

<br>

---

## 📂 Structure

```
my-ecommerce-api/
│
├── app/
│    ├── __init__.py                   # Factory Flask (+ Blueprints)
│    ├── errors_handlers.py
│    ├── run.py                        # Point d’entrée API
│    ├── spec.py                       # Point d'entrée Swagger
│    │
│    ├── core/                         # Middleware sécurité (JWT, accès, error handlers)
│    │    ├── __init__.py
│    │    ├── auth_decorators.py
│    │    ├── auth_utils.py
│    │    │
│    │    └── exceptions/
│    │        ├── app_errors.py
│    │        ├── errors_maps.py
│    │        └── orm_errors.py
│    │
│    ├── database/                     # ORM SQLAlchemy (gestion base/sessions)
│    │    ├── __init__.py
│    │    ├── base.py
│    │    ├── db_manager.py
│    │    └── sessions.py
│    │
│    ├── models/                       # Modèles SQLAlchemy
│    │    ├── __init__.py
│    │    ├── items.py
│    │    ├── orders.py
│    │    ├── products.py
│    │    └── users.py
│    │
│    ├── routes/                       # Routes (`api/auth`, `/api/produits*`, `/api/commandes*`)
│    │    ├── __init__.py
│    │    ├── auth_routes.py
│    │    ├── main_routes.py
│    │    ├── order_routes.py
│    │    └── product_routes.py
│    │
│    ├─── services/                    # Logique métier (+ validation JSON)
│    │    ├── __init__.py
│    │    ├── order_services.py
│    │    └── product_services.py
│    │
│    └── schemas/                      # Schemas (validation json, erreurs)
│         ├── __init__.py
│         ├── order_schemas.py
│         ├── product_schemas.py
│         ├── user_schemas.py
│         └── errors/
│              ├── __init__.py
│              ├── errors_schemas.py
│              ├── json_schemas.py
│              ├── order_errors.py
│              ├── product_errors.py
│              └── user_errors.py
│
├── tests/                             # Tests unitaires (+ fixtures)
│    ├── __init__.py
│    ├── conftest.py
│    ├── report.html
│    ├── test_orders.py
│    ├── test_products.py
│    └── test_users.py
│
├── database/                          # Base SQLite (local)
│    └── ecommerce.db
│
├── docs/                              # Documentations API / Tests      
│    ├── api_endpoints.md
│    ├── tests.md
│    ├── utils/
│    │    ├── api_utils.py
│    │    ├── fake_seeds.py
│    │    └── Flask_notebook.ipynb
│    │
│    └── img/
│         ├── server-flask.png
│         ├── results_order_tests.png
│         ├── results_product_tests.png
│         ├── results_user_tests.png
│         ├── redoc_home.png
│         ├── scalar_home.png
│         ├── scalar_register.png
│         ├── swagger_home.png
│         └── swagger_login.png
│
│
├── .gitignore
├── .env_template                      # Variables environnement
├── config.py                          # Configuration (Flask/SQLAlchemy + env)
├── pytest.ini                         # Configuration Pytest
├── requirements.txt                   # Dépendances python
└── README.md
```

<br>

### ⚙️ Prérequis

L'implémentation du code nécessite :

- Python >= 3.12  
- conda / virtualenv + pip  

<br>

> L'utilisation de l'outil SQLite (DB Browser) est optionnelle; elle permet néanmoins de vérifier :
> 
> - le schéma de la Base,  
> - la création des tables,  
> - les données enregistrées, modifiées ou supprimées.  

<br>

### 🚀 Installation (Conda, Linux/Windows)

1. Clonez le projet

```bash
git clone https://github.com/filrouge/my-ecommerce-api.git
cd my-ecommerce-api
```

2. Créez et activez l'environnement virtuel

```bash
# Conda
conda venv -n api_venv
conda activate api_venv

# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Installez les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

### 🔧 Configuration

Une fois le projet cloné et l'environnement crée, faites une copie du fichier `.env__template`...
Ensuite nommez le `.env` et modifiez ensuite les paramêtres du fichier `.env` avec vos propres valeurs :  

```
JWT_KEY=votre-nouvelle-clé  
ALGORITHM=votre-algorithme  
DATABASE_URL=votre-base-de-donnes  
FLASK_ENV=votre-nouvel-environnement  
```

<br>

### ▶️ Lancement

Exécutez `python app.app.py` ou `flask run --debug`.  

![Server Flask](docs/img/server-flask.png)

<br>

> 🌐 API accessible sur http://127.0.0.1:5000  
> 
> ⚠️ Lancez le serveur en mode DEBUG pour développement (ou test) uniquement

<br>

---

## 📄 Documentation API

La documentation, disponible sur les URLs suivants, est générée avec la librairie Spectree et le framework Pydantic :  
- Swagger UI : http://localhost:5000/apidoc/swagger  
- Redoc : http://localhost:5000/apidoc/redoc  
- Scalar: http://localhost:5000/apidoc/scalar/  
  
Le prochain tableau synthétise les *body* attendus pour les principales fonctionnalités (.e. endpoints); ces exemple sont également disponibles sous le format OpenAPI JSON (http://localhost:5000/apidoc/openapi.json).  

| Fonctionnalité                       | Body |
|--------------------------------------|---------|
| Inscription                          | ``` {"email": "client@test.com", "nom":"clienttestcom", "password":"secret"} ``` |
| Connexion                            | ``` {"email": "admin@test.com", "password":"password"} ``` |
| Création de produit                  | ``` {"nom": "Produit Test", "prix":99.9, "quantite_stock":5} ``` |
| Mise à jour d'un produit             | ``` {"nom": "Produit Modifié", "prix":79.9, "quantite_stock":10} ``` |
| Création de commande                 | ``` { "adresse_livraison": "4 rue d'ici, 75000 Paname", "produits": [{"id": 1, "quantite": 2},{"id": 2, "quantite": 1}] } ``` |
| Mise à jour statut d’une commande    | ``` {"statut": "Expédiée"} ``` |

<br>

> 📂 Consultez [api_endpoints.md](docs/api_endpoints.md) pour plus d’informations.

<br>

---

## 🧪 Tests

Les tests unitaires s'appuient sur le framework `pytest` et couvrent les points :  

    ✅ *Utilisateurs* : inscription, authentification, autorisation  
    ✅ *Produits* : création, consultation, suppression  
    ✅ *Commandes* : création, consultation, modification  
    ✅ *Erreurs* : validation, restriction, exécution  

<br>

> 📂 Consultez [tests.md](docs/tests.md) pour plus d’informations (et voir les résultats des tests réalisés en base mémoire).

<br>

---

#### 📌 Todo
> - Axes d'améliorations:
>     - Logger pour monitoring
>     - Docker (containerisation)
