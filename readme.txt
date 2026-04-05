# AP-HB Encryption Agent

## 1. Présentation générale

Ce projet implémente un agent logiciel dédié au chiffrement automatique de répertoires contenant des données sensibles. Il s’inscrit dans une démarche de sécurisation des systèmes d’information, notamment dans des contextes manipulant des données critiques telles que les données de santé ou financières.

L’objectif principal est de garantir la confidentialité et l’intégrité des données stockées, en assurant qu’aucune information exploitable ne puisse être obtenue en cas d’accès non autorisé ou d’exfiltration.

---

## 2. Architecture de la solution

L’agent repose sur des mécanismes cryptographiques reconnus et conformes aux standards actuels de sécurité.

| Composant                 | Description                            |
| ------------------------- | -------------------------------------- |
| Algorithme de chiffrement | AES-256-GCM (Authenticated Encryption) |
| Dérivation de clé         | PBKDF2-HMAC-SHA256                     |
| Nombre d’itérations       | 100 000                                |
| Taille du sel             | 32 octets aléatoires                   |
| Vecteur d’initialisation  | 12 octets aléatoires                   |
| Intégrité                 | Tag GCM 128 bits                       |
| Langage                   | Python 3.x                             |
| Bibliothèque              | cryptography (module hazmat)           |
| Journalisation            | Logs horodatés                         |

L’utilisation du mode GCM permet d’assurer simultanément la confidentialité et l’intégrité des données, en détectant toute altération des fichiers chiffrés.

---

## 3. Fonctionnalités principales

L’agent propose les fonctionnalités suivantes :

* Chiffrement automatique des fichiers contenus dans un répertoire
* Déchiffrement contrôlé des fichiers précédemment chiffrés
* Traitement récursif des sous-répertoires
* Génération d’un journal d’audit des opérations effectuées
* Suppression des fichiers en clair après chiffrement

---

## 4. Structure du projet

```id="n8k3qd"
.
├── aphb_agent.py
├── aphb_encryption_agent.log
├── test_data/
└── README.md
```

---

## 5. Installation

### 5.1 Prérequis

* Python 3.8 ou supérieur
* Gestionnaire de paquets pip

### 5.2 Installation des dépendances

```bash id="q1z9lf"
pip install cryptography
```

---

## 6. Utilisation

### 6.1 Chiffrement d’un répertoire

```bash id="p4t9s2"
python aphb_agent.py /chemin/vers/dossier --mode encrypt
```

### 6.2 Déchiffrement d’un répertoire

```bash id="k2v7mx"
python aphb_agent.py /chemin/vers/dossier --mode decrypt
```

Lors de l’exécution, une passphrase est demandée de manière sécurisée via l’entrée standard.

---

## 7. Automatisation

L’agent peut être intégré dans des mécanismes d’ordonnancement afin d’automatiser les opérations de chiffrement.

### Exemple sous Linux (cron)

```bash id="d7c1be"
0 2 * * * /usr/bin/python3 /opt/aphb/aphb_agent.py /data/sensibles --mode encrypt
```

Cette configuration permet d’exécuter le chiffrement quotidiennement à 02h00.

---

## 8. Journalisation et audit

Les opérations sont enregistrées dans un fichier de log :

```id="m5x0sj"
aphb_encryption_agent.log
```

Chaque entrée contient :

* Horodatage
* Niveau de log
* Description de l’opération

Ce mécanisme permet d’assurer la traçabilité des actions effectuées par l’agent.

---

## 9. Aspects de sécurité

Le système repose sur plusieurs garanties de sécurité :

* Utilisation d’un algorithme de chiffrement robuste (AES-256)
* Dérivation de clé sécurisée via PBKDF2
* Génération de paramètres cryptographiques aléatoires (sel, IV)
* Détection des altérations grâce au mode GCM
* Suppression des fichiers en clair après chiffrement

Il est recommandé de :

* Utiliser une passphrase forte
* Ne jamais stocker la passphrase en clair
* Mettre en place une gestion sécurisée des secrets en environnement de production

---

## 10. Déploiement

L’agent peut être déployé dans différents environnements :

* Systèmes Linux via cron
* Environnements Windows via Task Scheduler
* Conteneurs Docker (extension possible)

---

## 11. Licence

Ce projet est distribué sous licence MIT, autorisant l’utilisation, la modification et la redistribution du code.

---

## 12. Références

* NIST, Advanced Encryption Standard (AES)
* RFC 8018 – PBKDF2
* Documentation officielle de la bibliothèque cryptography

---

## 13. Perspectives d’évolution

Plusieurs axes d’amélioration peuvent être envisagés :

* Intégration de mécanismes d’intelligence artificielle pour la détection automatique de données sensibles
* Ajout d’une interface utilisateur
* Intégration avec des systèmes de supervision (SIEM, SOC)
* Gestion multi-utilisateurs avec contrôle d’accès

---
## 14. Validation et procédure de test

Afin de vérifier le bon fonctionnement de l’agent de chiffrement, une procédure de test simple peut être mise en œuvre.

### 14.1 Préparation

Créer un répertoire de test contenant un ou plusieurs fichiers :

```bash
mkdir test_data
echo "donnée sensible" > test_data/test.txt
```

---

### 14.2 Test de chiffrement

Exécuter la commande suivante :

```bash
python aphb_agent.py test_data --mode encrypt
```

Résultat attendu :

* Le fichier `test.txt` est supprimé
* Un fichier `test.txt.aphb` est généré
* Une entrée est ajoutée dans le fichier de log

---

### 14.3 Test de déchiffrement

Exécuter :

```bash
python aphb_agent.py test_data --mode decrypt
```

Résultat attendu :

* Le fichier `test.txt.aphb` est supprimé
* Le fichier original `test.txt` est restauré
* Le contenu du fichier est identique à l’original

---

### 14.4 Vérification d’intégrité

Modifier manuellement un fichier chiffré :

```bash
echo "corruption" >> test_data/test.txt.aphb
```

Puis tenter un déchiffrement.

Résultat attendu :

* Échec du déchiffrement
* Levée d’une exception (authentification GCM invalide)

---

### 14.5 Analyse des logs

Consulter le fichier :

```bash
cat aphb_encryption_agent.log
```

Vérifier la présence des entrées :

* ENCRYPTED
* DECRYPTED
* ERROR (le cas échéant)

---

### 14.6 Critères de validation

Le système est considéré comme valide si :

* Les fichiers sont correctement chiffrés et déchiffrés
* Aucun fichier en clair ne subsiste après chiffrement
* Toute modification des données chiffrées est détectée
* Les logs reflètent fidèlement les opérations effectuées

---
