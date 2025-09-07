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

**API REST** construite avec les librairies **Flask**, **SQLAlchemy** et **JWT**, et reposant sur une architecture modulaire avec séparation des responsabilités.

Fonctionnalités principales :

- 👤 *Gestion des utilisateurs / permissions*  
- 📦 *Gestion des produits*  
- 🛒 *Gestion des commandes*  
<br>

> 📂 Consultez la documentation [docs/api_endpoints.md](docs/api_endpoints.md) pour plus d’informations sur l'architecture et les fonctionnalités de l'API.

<br>

---

## 📂 Structure du projet

```
my-ecommerce-api/
│
├── app.py                      # Point d’entrée API (+ Blueprints)
├── config.py                   # Configuration Flask/SQLAlchemy
│
├── core/                       # Middleware sécurité (JWT, accès, validation JSON, error handlers)
│   ├── __init__.py
│   ├── auth_utils.py
│   ├── auth.py
│   ├── errors_handlers.py
│   └── utils.py
│
├── database/                   # (optionnel pour les tests)
│
├── docs/                       # Documentations API / Tests
│   ├── api_endpoints.md
│   └── tests.md
│
├── model/                      # ORM SQLAlchemy (mdolèles, gestion des sessions)
│   ├── __init__.py
│   ├── database.py
│   ├── sessions.py
│   └── models.py
│
├── routes/                     # Routes (`api/auth`, `/api/produits*`, `/api/commandes*`)
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── main_routes.py
│   ├── order_routes.py
│   └── product_routes.py
│
├── services/                   # Logique métier
│   ├── __init__.py
│   ├── product_utils.py
│   └── order_utils.py
│
├── tests/                      # Tests unitaires/fonctionnels (+ fixtures)
│   ├── __init__.py
│   ├── conftest.py
│   ├── report.html
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
│
├── .gitignore
├── requirements.txt            # Liste des dépendances python
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

Exécutez `python app.py` ou `flask run --debug`.  

![Server Flask](server-flask.png)

<br>

> 🌐 API accessible sur http://127.0.0.1:5000  
> 
> ⚠️ Lancez le serveur en mode DEBUG pour développement uniquement

<br>

---

## 📄 Documentation API

Ce tableau offre une synthèse des *body* attendus pour les fonctionnalités principales.

| Fonctionnalité                       | Body |
|--------------------------------------|---------|
| Inscription                          | ``` {"email": "client@test.com", "nom":"clienttestcom", "password":"secret"} ``` |
| Connexion                            | ``` {"email": "admin@test.com", "password":"password"} ``` |
| Création de produit                  | ``` {"nom": "Produit Test", "prix":99.9, "quantite_stock":5} ``` |
| Mise à jour d'un produit             | ``` {"nom": "Produit Modifié", "prix":79.9, "quantite_stock":10} ``` |
| Création de commande                 | ``` { "adresse_livraison": "4 rue d'ici, 75000 Paname", "produits": [{"id": 1, "quantite": 2},{"id": 2, "quantite": 1}] } ``` |
| Mise à jour statut d’une commande    | ``` {"statut": "Expédiée"} ``` |

<br>

> 📂 Consultez la documentation [docs/api_endpoints.md](docs/api_endpoints.md) pour plus d’informations sur les endpoints (routes, formats JSON, exemples cURL...), et la gestion des erreurs (couverture, cas, messages...).

<br>

---

## 🧪 Tests

Les tests unitaires s'appuient sur la librairie `pytest` et couvrent les points :  

    ✅ *Authentification / Autorisation* : inscription, login, rôles  
    ✅ *Produits* : création, consultation, suppression  
    ✅ *Commandes* : création, consultation, modification  
    ✅ *Erreurs* : validation, restriction, exécution  

<!-- TODO : pytest.ini + fixture parametrize pour alléger -->

<br>

> 📂 Consultez [docs/tests.md](docs/tests.md) pour plus d’informations sur les tests (couverture fonctionnalités / erreurs).

<br>

---

#### 📌 TODO
> - Refactoring des tests (fixtures)
> - Add-ons:
>     - Logger & Monitoring
>     - Jeux de données (script `seed_data.py`)
>     - Tests d’intégration end-to-end
>     - Dockérisation
>     - Intégration CI/CD (`GitHub Actions`)