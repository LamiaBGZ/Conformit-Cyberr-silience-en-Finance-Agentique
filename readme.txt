# AP-HB Encryption Agent

## Présentation générale

Ce projet a été réalisé dans le cadre de l’atelier « Conformité et Cyber-résilience en Finance Agentique ».

Il s’inscrit dans un scénario où l’établissement hospitalier AP-HB a subi une cyberattaque majeure, mettant en danger la confidentialité des données sensibles des patients.

L’objectif est de renforcer la cyber-résilience du système d’information en mettant en place un agent capable de protéger automatiquement les données sensibles.

L’agent garantit que « aucune donnée ne sort sous forme lisible », même en cas d’exfiltration après une cyberattaque.

---

## Objectif

L’objectif principal est de :

- garantir la confidentialité des données sensibles ;
- empêcher toute exploitation des données en cas d’accès non autorisé ;
- assurer la protection des données de santé conformément aux exigences de sécurité et de conformité, notamment le RGPD.

---

## Architecture de la solution

L’agent repose sur des mécanismes cryptographiques robustes et conformes aux standards actuels.

| Composant | Description |
|-----------|-------------|
| Algorithme de chiffrement | AES-256-GCM |
| Dérivation de clé | PBKDF2-HMAC-SHA256 |
| Nombre d’itérations | 100 000 |
| Taille du sel | 32 octets |
| Vecteur d’initialisation | 12 octets |
| Intégrité | Tag GCM 128 bits |
| Langage | Python 3 |
| Bibliothèque | cryptography |
| Journalisation | Logs horodatés |

Le mode GCM permet d’assurer la confidentialité et l’intégrité des données.

---

## Fonctionnalités principales

- chiffrement automatique des fichiers d’un répertoire ;
- déchiffrement sécurisé des fichiers ;
- traitement récursif des sous-répertoires ;
- journalisation des opérations ;
- suppression des fichiers en clair après chiffrement.

---

## Structure du projet

.
├── apbh_agent.py  
├── test_agent.py  
├── requirements.txt  
├── Dockerfile  
├── README.md  
├── test_data/  
└── logs/  

---

## Installation

Prérequis :
- Python 3.8 ou supérieur
- pip

Installation des dépendances :

pip install -r requirements.txt

---

## Utilisation

Chiffrement :

python3 apbh_agent.py /chemin/vers/dossier --mode encrypt

Déchiffrement :

python3 apbh_agent.py /chemin/vers/dossier --mode decrypt

Une passphrase est demandée de manière sécurisée lors de l’exécution.

---

## Exécution avec Docker

Construction :

docker build -t apbh-agent .

Exécution :

docker run --rm apbh-agent

---

## Automatisation

Exemple avec cron sous Linux :

0 2 * * * /usr/bin/python3 /opt/apbh/apbh_agent.py /data/sensibles --mode encrypt

---

## Journalisation

Les opérations sont enregistrées dans :

logs/apbh_encryption_agent.log

Chaque entrée contient :
- horodatage ;
- niveau ;
- description de l’action.

---

## Sécurité

Le système garantit :
- chiffrement AES-256 robuste ;
- dérivation sécurisée des clés ;
- génération aléatoire des paramètres ;
- détection des altérations ;
- suppression des données en clair.

Recommandations :
- utiliser une passphrase forte ;
- ne jamais stocker la clé en clair ;
- utiliser un gestionnaire de secrets.

Le système contribue à la conformité avec le RGPD.

---

## Déploiement

Possible sur :
- Linux ;
- Windows ;
- Docker.

---

## Validation et tests

Préparation :

mkdir test_data  
echo "donnée sensible" > test_data/test.txt  

Test chiffrement :

python3 apbh_agent.py test_data --mode encrypt  

Résultat attendu :
- fichier original supprimé ;
- fichier chiffré créé ;
- log généré.

Test déchiffrement :

python3 apbh_agent.py test_data --mode decrypt  

Résultat attendu :
- fichier restauré ;
- contenu intact.

Test d’intégrité :

echo "corruption" >> test_data/test.txt.enc  

Résultat attendu :
- échec du déchiffrement ;
- détection d’altération.

---

## Code source

https://github.com/LamiaBGZ/Conformit-Cyberr-silience-en-Finance-Agentique

---

## Licence

Licence MIT.

---

## Perspectives d’amélioration

- intégration d’IA pour détecter les données sensibles ;
- gestion avancée des clés ;
- interface utilisateur ;
- intégration avec SIEM/SOC ;
- amélioration des tests.
