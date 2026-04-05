# AP-HB Encryption Agent

## Présentation générale

Ce projet a été réalisé dans le cadre de l’atelier « Conformité et Cyber-résilience en Finance Agentique ».

Il s’inscrit dans un scénario où l’établissement hospitalier AP-HB a subi une cyberattaque majeure, mettant en danger la confidentialité des données sensibles des patients.

L’objectif est de renforcer la cyber-résilience du système d’information en mettant en place un agent capable de protéger automatiquement les données sensibles.

L’agent garantit que « aucune donnée ne sort sous forme lisible », même en cas d’exfiltration après une cyberattaque.

## Objectif

- garantir la confidentialité des données sensibles
- empêcher toute exploitation des données
- assurer la conformité au RGPD

## Fonctionnalités

- chiffrement automatique des fichiers
- déchiffrement sécurisé
- journalisation
- suppression des fichiers en clair

## Installation

pip install -r requirements.txt

## Utilisation

python3 apbh_agent.py /chemin --mode encrypt
python3 apbh_agent.py /chemin --mode decrypt

## Code source

https://github.com/LamiaBGZ/Conformit-Cyberr-silience-en-Finance-Agentique
