cat > README.md << 'EOF'
# AP-HB Encryption Agent

## 1. Présentation générale

Ce projet implémente un agent logiciel dédié au chiffrement automatique de répertoires contenant des données sensibles.

Il s’inscrit dans un scénario où l’établissement hospitalier AP-HB a subi une cyberattaque majeure, mettant en danger la confidentialité des données de santé et financières.

L’objectif principal est de garantir la confidentialité et l’intégrité des données stockées, en assurant qu’aucune information exploitable ne puisse être obtenue en cas d’accès non autorisé ou d’exfiltration.

L’agent garantit que « aucune donnée ne sort sous forme lisible », même en cas de compromission du système.

---

## 2. Architecture de la solution

L’agent repose sur des mécanismes cryptographiques reconnus et conformes aux standards actuels de sécurité.

- Algorithme : AES-256-GCM
- Dérivation de clé : PBKDF2-HMAC-SHA256
- Itérations : 100 000
- Sel : 32 octets
- IV : 12 octets
- Intégrité : tag GCM 128 bits
- Langage : Python 3
- Bibliothèque : cryptography
- Logs : horodatés

---

## 3. Fonctionnalités principales

- chiffrement automatique des fichiers contenus dans un répertoire
- déchiffrement sécurisé des fichiers
- traitement récursif des sous-répertoires
- journalisation des opérations
- suppression des fichiers en clair après chiffrement

---

## 4. Structure du projet

apbh_agent.py
apbh_encryption_agent.log
test_data/
README.md

---

## 5. Installation

pip install cryptography

---

## 6. Utilisation

Chiffrement :
python3 apbh_agent.py /chemin/vers/dossier --mode encrypt

Déchiffrement :
python3 apbh_agent.py /chemin/vers/dossier --mode decrypt

---

## 7. Automatisation

0 2 * * * /usr/bin/python3 /opt/apbh/apbh_agent.py /data/sensibles --mode encrypt

---

## 8. Journalisation

apbh_encryption_agent.log

---

## 9. Sécurité

- chiffrement AES-256
- dérivation sécurisée
- paramètres aléatoires
- détection des altérations
- suppression des données en clair

Le système contribue à la conformité RGPD.

---

## 10. Déploiement

- Linux
- Windows
- Docker

---

## 11. Licence

MIT

---

## 12. Perspectives

- intégration IA
- gestion avancée des clés
- interface utilisateur
- intégration SIEM / SOC

---

## 13. Tests

mkdir test_data
echo "donnée sensible" > test_data/test.txt

python3 apbh_agent.py test_data --mode encrypt
python3 apbh_agent.py test_data --mode decrypt
EOF
