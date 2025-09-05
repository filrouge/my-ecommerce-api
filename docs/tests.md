# 🧪 Documentation des tests

## 📂 Structure des tests

Les tests unitaires s'appuient sur des fichiers dédiés à chaque domaine de routes.

```
tests/
├── conftest.py          # Fixtures pytest (BDD, client Flask...)
│
├── test_users.py        # Tests Authentification / Autorisation
├── test_products.py     # Tests CRUD Produits
└── test_orders.py       # Tests CRUD Commandes
```


> ⚠️ Ces tests sont configurés pour être exécutés en mémoire (`:memory:`) depuis la configuration `conftest.py`. Pour une utilisation en PROD ou sur une base de données dédiée, modifiez les configurations suivantes:
`app.config["TESTING"] = True`
`engine = create_engine("sqlite:///:memory:", echo=False)`

<br>

## ▶️ Exécution des tests

Executez les commandes suivantes pour lancer les tests voulus depuis la racine du projet.

Ajoutez l'option `--maxfail=<int> --disable-warnings` si besoin pour stopper les tests après `<int>` echecs:

- `pytest -v` : → cible tous les tests
- `pytest -v tests/test_users.py` : → cible un seul fichier de tests
- `pytest -vv tests/test_users.py` : → affiche le détail des assertions
- `pytest -v tests/test_users.py::TestLogin` : → cible un seul module de tests
- `pytest -v tests/test_users.py::TestAdminAccess::test_access_denied` : → cible un test spécifique

<br>

## ℹ️ Couverture

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
    - Autorisé pour `admin`
    - Autorisé pour `client`
    - Refusé pour autre que `admin`
    - Refusé pour autre que `client` propriétaire

<br>

- 📦 Produits (`/api/produits`)
  - Liste de tous les produits
  - Recherche par nom, catégorie ou disponibilité
  - Création de produit (`admin` only)
  - Mise à jour de produit (`admin` only)
  - Suppression de produit (`admin` only)

<br>

- 🛒 Commandes (`/api/commandes`)
  - Création de commande (`client` only)
  - Consultation des commandes (`client` propriétaire)
  - Consultation de tous les commandes (`admin` only)
  - Consultation des lignes d'une commande  # (`public` !!!)
  - Modification de statut d’une commande (`admin` only)

<br>

> ℹ️ _Pour générer un rapport de tests (`<mon-rapport>.html`), installez la librairie avec `pip install pytest-html` puis executez la commande suivante :_
`pytest -vv test_products.py --html=<mon-rapport>.html --self-contained-html`
