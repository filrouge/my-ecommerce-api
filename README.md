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

**API REST** construite avec **Flask**, **SQLAlchemy**, **JWT** et **Pydantic**, et reposant sur une architecture modulaire qui couvrent les fonctionnalités principales :

- 👤 *Gestion des utilisateurs*  
- 📦 *Gestion des produits*  
- 🛒 *Gestion des commandes*  
  

La séparation des responsabilités est assurée comme suit :

- logique HTTP (request/response, status code): `routes/`
- logique métier et manipulation de la base (g.session): `services/`
- centralisation des entités/relations SQLAlchemy: `model/`
- socle d'infrastructure commun (connexion, JWT, sécurité): `core/`
- validation et typage automatique (Pydantic): `schemas/`

<br>

> 📂 Consultez [api_endpoints.md](docs/endpoints/api_endpoints.md) pour plus d’informations sur l'architecture et les fonctionnalités de l'API.

<br>

---

## 📂 Structure

```
my-ecommerce-api/
│
├── app/
│    ├── __init__.py                 # Factory Flask (+ Blueprints)
│    ├── app.py                      # Point d’entrée API
│    │
│    ├── core/                       # Middleware sécurité (JWT, accès, error handlers)
│    │    ├── __init__.py
│    │    │
│    │    ├── auth_utils.py
│    │    ├── errors_handlers.py
│    │    ├── permissions.py
│    │    │
│    │    └── exceptions/
│    │         ├── app_errors.py
│    │         └── orm_errors.py
│    │
│    ├── database/                    # ORM SQLAlchemy (gestion de la base/sessions)
│    │    ├── __init__.py
│    │    │
│    │    ├── base.py
│    │    ├── db_manager.py
│    │    └── sessions.py            
│    │
│    ├── models/                      # Modèles SQLAlchemy
│    │    ├── __init__.py
│    │    │
│    │    ├── items.py
│    │    ├── orders.py
│    │    ├── products.py
│    │    └── users.py
│    │
│    ├── routes/                      # Routes (`api/auth`, `/api/produits*`, `/api/commandes*`)
│    │    ├── __init__.py
│    │    │
│    │    ├── auth_routes.py
│    │    ├── main_routes.py
│    │    ├── order_routes.py
│    │    └── product_routes.py
│    │
│    └── services/                    # Logique métier (+ validation JSON)
│         ├── __init__.py
│         │
│         ├── order_services.py
│         ├── product_servicess.py
│         └── validators.py
│    
├── tests/                       # Tests unitaires/fonctionnels (+ fixtures)
│    ├── __init__.py
│    │
│    ├── conftest.py
│    ├── report.html
│    ├── test_orders.py
│    ├── test_products.py
│    └── test_users.py
│
│
├── docs/                             # Documentations API / Tests      
│    ├── api_endpoints.md
│    ├── tests.md
│    └── img/
│        ├── server-flask.png
│        └── others_to_come.png
│
├── .gitignore
├── .env_template                     # Liste les variables environnement
├── config.py                         # Configuration (Flask/SQLAlchemy + env)
├── pytest.ini                        # Configuration Pytest
├── requirements.txt                  # Liste des dépendances python
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

Une fois le projet cloné et l'environnement crée, modifiez le fichier `config.py` avec vos propres valeurs :

```
DATABASE_URL=sqlite:///path-to-database.db

JWT_SECRET_KEY=your-jwt-secret
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

La documentation, disponible sur les URLs suivants, a été générée avec la librairie Spectree et le framework Pydantic :  
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

> 📂 Consultez [api_endpoints.md](docs/endpoints/api_endpoints.md) pour plus d’informations.

<br>

---

## 🧪 Tests

Les tests unitaires s'appuient sur le framework `pytest` et couvrent les points :  

    ✅ *Utilisateurs* : inscription, authentification, autorisation  
    ✅ *Produits* : création, consultation, suppression  
    ✅ *Commandes* : création, consultation, modification  
    ✅ *Erreurs* : validation, restriction, exécution  

<br>

> 📂 Consultez [tests.md](docs/tests/tests.md) pour plus d’informations (et voir les résultats des tests réalisés en base mémoire).

<br>

---

#### 📌 TODO
> - Futurs Add-ons:
>     - OOP (si léger refactoring)
>     - Logger & Monitoring
>     - Dockérisation