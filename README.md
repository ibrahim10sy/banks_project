## 🏦 Banks ETL Project

Ce projet Python automatise l'extraction, la transformation et le chargement (ETL) des données des plus grandes banques du monde depuis Wikipedia. Les données sont nettoyées, enrichies par des conversions de devises, sauvegardées au format CSV, et stockées dans une base de données **MySQL** locale (XAMPP).

### 🎯 Objectif

* Extraire les données de capitalisation boursière des grandes banques depuis [Wikipedia](https://en.wikipedia.org/wiki/List_of_largest_banks)
* Transformer les données pour inclure la conversion en différentes devises (GBP, EUR, INR)
* Stocker les résultats :

  * dans un fichier `.csv`
  * dans une base de données **MySQL** via SQLAlchemy

### 🧱 Architecture du projet

```text
├── banks_project.py         # Script principal ETL
├── Largest_banks_data.csv   # CSV de transformation (intermédiaire)
├── banks_data.csv           # CSV final
├── code_log.txt             # Journal de logs de l’ETL

```

### 🛠️ Technologies utilisées

* Python 3.10+
* [pandas](https://pandas.pydata.org/)
* [requests](https://requests.readthedocs.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [MySQL (XAMPP)](https://www.apachefriends.org/fr/index.html)
* [PyMySQL](https://pypi.org/project/PyMySQL/)

### ⚙️ Étapes ETL

1. **Extraction**

   * Récupération de la table HTML des plus grandes banques sur Wikipedia.

2. **Transformation**

   * Nettoyage des valeurs
   * Conversion de la capitalisation boursière en :

     * Livres sterling (GBP)
     * Euros (EUR)
     * Roupies indiennes (INR)

3. **Chargement**

   * Export vers un fichier CSV (`banks_data.csv`)
   * Insertion dans la base de données MySQL (`banksdb`)

4. **Requêtes SQL**

   * Affichage des premières lignes
   * Moyenne des capitalisations en GBP
   * Top 5 des banques par capitalisation USD

### 📝 Exemple de log dans `code_log.txt`

```
ETL Job Started,2025-06-24 11:00:00
Extract phase Started,2025-06-24 11:00:01
Extract phase Ended,2025-06-24 11:00:03
...
SQL Query Ended,2025-06-24 11:00:12
ETL Job Ended,2025-06-24 11:00:12
```


### ✅ Instructions

1. Installez les dépendances :

```bash
pip install pandas requests beautifulsoup4 sqlalchemy pymysql
```

2. Lancez **XAMPP** et démarrez **Apache** + **MySQL**
3. Créez la base de données dans phpMyAdmin :

   * Nom : `banksdb`
4. Modifiez le mot de passe dans ce fichier si nécessaire :

```python
engine = create_engine("mysql+pymysql://root:<votre_mot_de_passe>@localhost/banksdb", future=True)
```

5. Exécutez le script :

```bash
python banks_project.py
```

---

### 📌 Remarques

* Le script crée automatiquement la table `Largest_banks`
* Tous les événements sont journalisés dans `code_log.txt`
* L'extraction est sensible aux changements de structure sur Wikipedia
