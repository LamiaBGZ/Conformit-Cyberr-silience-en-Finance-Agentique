# AP-HB Encryption Agent

## Présentation générale

Ce projet a été réalisé dans le cadre de l’atelier « Conformité et Cyber-résilience en Finance Agentique ».

Il s’inscrit dans un scénario où l’établissement hospitalier AP-HB a subi une cyberattaque majeure, mettant en danger la confidentialité des données sensibles des patients.

L’objectif est de renforcer la cyber-résilience du système d’information en mettant en place un agent capable de protéger automatiquement les données sensibles.

L’agent garantit que **« aucune donnée ne sort sous forme lisible »**, même en cas d’exfiltration après une cyberattaque.

---

## Objectif

L’objectif principal est de :

- garantir la confidentialité des données sensibles ;
- empêcher toute exploitation des données en cas d’accès non autorisé ;
- assurer la protection des données de santé conformément aux exigences de sécurité et de conformité, notamment le RGPD.

---

## Architecture de la solution

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

---

## Fonctionnalités principales

- chiffrement automatique des fichiers d’un répertoire
- déchiffrement sécurisé des fichiers
- traitement récursif des sous-répertoires
- journalisation des opérations
- suppression des fichiers en clair après chiffrement

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

pip install -r requirements.txt

---

## Utilisation

Chiffrement :

python3 apbh_agent.py /chemin/vers/dossier --mode encrypt

Déchiffrement :

python3 apbh_agent.py /chemin/vers/dossier --mode decrypt

---

## Docker

docker build -t apbh-agent  
docker run --rm apbh-agent  

---

## Automatisation (cron)

0 2 * * * /usr/bin/python3 /opt/apbh/apbh_agent.py /data/sensibles --mode encrypt

---

## Logs

logs/apbh_encryption_agent.log

---

## Code source

https://github.com/LamiaBGZ/Conformit-Cyberr-silience-en-Finance-Agentique

---

## Licence

MIT

---

## Perspectives

- intégration IA
- gestion avancée des clés
- interface utilisateur
- intégration SIEM / SOC
