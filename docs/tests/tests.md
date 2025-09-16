# Documentation des tests

L’ensemble des tests unitaires est écrit avec le framework  **pytest** et couvre les fonctionnalités principales de l’API :  
- Authentification (`test_user.py`)  
- Produits (`test_product.py`)  
- Commandes (`test_order.py`)  

---

## 📂 Organisation

Ces tests s'appuient sur des fichiers dédiés à chaque domaine de routes.  
Le fichier `conftest.py` centralise les **fixtures communes** qui permette de pour générer un client Flask et une session SQLAlchemy (`test_client`), des tokens JWT admin et client (`admin_token`, `client_token`) et de fournir un jeu de données produits/commandes (`feed_product`, `feed_order`) injectés dans la base en mémoire (session isolée avec create/drop des tables à chaque test). 

```
tests/
├── conftest.py          → Fixtures (instance isolée, client Flask et session BdD en mémoire...)
│
├── test_users.py        → couvre les tests inscription, connexion (+ token JWT) et autorisation
├── test_products.py     → couvre les test Produits (création, consultation, modification, suppression)
└── test_orders.py       → couvre les tests Commandes (création, consultation, mise à jour)
```

<br>

> ⚠️ Les tests sont exécutés en base mémoire (`:memory:`).
> Modifiez la ligne suivante (depuis `conftest.py`) pour utiliser une base dédiée (fichier `e-commerce.db`) :
`engine = create_engine("sqlite:///:memory:", echo=False)`  

<!-- 
au niveau config.py ou __init__.py sinon terminal via:
export FLASK_ENV = "dev"
    # `app.config["TESTING"] = True`  
    # `app.config["DEBUG"] = True`  

"Ajouter rapport de couverture":
  `pytest --cov=mon_projet --cov-report=term-missing`
   pytest --cov=. --cov-report=term --cov-report=html
  `pytest --cov=core --cov=model --cov=routes --cov=services --cov-report=term --cov-report=html`

"Rapport de couverture": 
`pytest --cov=mon_projet --cov-report=term-missing`

A paramétrer dans `pytest.ini` !!!!
addopts = --cov=core --cov=model --cov=routes --cov=services --cov-report=term --cov-report=html
 -->



<br>

### ▶️ Exécution

Executez la commande suivante depuis la racine du projet pour lancer tous les tests, l'option `--maxfail=<int> --disable-warnings` permet de stopper la campagne de tests après `<int>` echecs:  
```bash
pytest -v
```

Executez les commandes suivantes selon la campagne de tests souhaitée.  
- `pytest -v tests/test_users.py` : → cible un seul fichier de tests  
- `pytest -vv tests/test_users.py` : → affiche le détail des assertions  
- `pytest -v tests/test_users.py::TestLogin` : → cible un seul module de tests  
- `pytest -v tests/test_users.py::TestAdminAccess::test_access_denied` : → cible un test spécifique

<br>

### ℹ️ Couverture

Les tests couvrent, entre-autres, les points suivants:

- 👤 Utilisateurs (admin, client ...)
    - Inscription (`/api/auth/register`)
      - Email unique
      - Mot de passe haché
      - Rôle (défaut = client)  
    - Connexion (`/api/auth/login`)
      - Validée avec token JWT renvoyé
      - Refusée si mauvais mot de passe  
    - Accès restreint (`/api/admin-only-route`)
      - Autorisé pour `admin` et/ou `client`
      - Refusé pour autre que `admin` ou `client` propriétaire

<br>

- 📦 Produits (`/api/produits`)
    - Liste de tous les produits
    - Recherche par nom, catégorie ou disponibilité
    - Création de produit (`admin`)
    - Mise à jour de produit (`admin`)
    - Suppression de produit (`admin`)

<br>

- 🛒 Commandes (`/api/commandes`)
    - Création de commande (`client`)
    - Consultation des commandes (`client` propriétaire)
    - Consultation de tous les commandes (`admin`)
    - Consultation des lignes d'une commande  (# `public` !!!)
    - Modification de statut d’une commande (`admin`)

<br>

> ℹ️ _Pour générer un rapport de tests (`<mon-rapport>.html`), installez `pytest-html` avec `pip install pytest-html`, puis executez :_  
`pytest -vv test_products.py --html=<mon-rapport>.html --self-contained-html`


Les copies d'écran suivantes indiquent les résultats des tests effectués en base mémoire :  

![Pytest_user](docs/tests/img/results_user_tests.png)  
  
![Pytest_product](docs/tests/img/results_product_tests.png)  
  
![Pytest_order](docs/tests/img/results_order_tests.png)
  
