# Documentation des tests

L’ensemble des tests unitaires est écrit avec **pytest** et couvre les fonctionnalités principales de l’API :  
- Authentification (`test_user.py`)  
- Produits (`test_product.py`)  
- Commandes (`test_order.py`)  

---

## 📂 Structure

Ces tests s'appuient sur des fichiers dédiés à chaque domaine de routes.
Le fichier `conftest.py` centralise les **fixtures partagées** pour générer un client Flask et une session SQLAlchemy (`test_client`), des tokens JWT admin et client (`admin_token`, `client_token`) et fournir un jeu de données produits/commandes injectés dans la base (`feed_product`, `feed_order`)  

```
tests/
├── conftest.py          → Fixtures (BDD, client Flask...)
│
├── test_users.py        → couvre la partie Utilisateurs (inscription, authentification, autorisation)
├── test_products.py     → couvre la partie Produits (liste, création, modification, suppression)
└── test_orders.py       → couvre la partie Commandes (création, consultation, mise à jour du statut)
```

<br>

> ⚠️ Ces tests sont configurés pour être exécutés en mémoire (`:memory:`) depuis `conftest.py`.
> Modifiez la ligne suivante pour utiliser une base dédiée (fichier `database_test.db`) :
`engine = create_engine("sqlite:///:memory:", echo=False)`  

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
      - Autorisé pour `admin`
      - Autorisé pour `client`
      - Refusé pour autre que `admin`
      - Refusé pour autre que `client` propriétaire

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



<br>

######## ℹ️ TODO ?
- Rapport de couverture : pytest --cov=.