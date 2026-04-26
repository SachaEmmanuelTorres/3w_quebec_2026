# IA Locale, Open Source et Agents RAG 🚀 (Version Stack Podman)

Présentation technique réalisée pour **3W Québec** à l'**UQAM** le **23 Avril 2026**.

## 📝 Description du Projet
Ce dépôt a été refactorisé pour passer de scripts Python isolés à une architecture conteneurisée robuste sous **Podman**. L'objectif est de déployer une stack complète pour la gestion, la création d'agents IA complexes et l'implémentation de pipelines RAG avancés via des outils d'orchestration spécialisés.

## 📅 Détails de la Présentation
- **Titre :** IA Locale, Open Source et Agents RAG : Souveraineté et Performance
- **Lieu :** UQAM - 3W Québec
- **Date :** 23 Avril 2026
- **Auteur :** Sacha Emmanuel Torres

## 🛠️ Stack Technique (Infrastructure Podman)
L'architecture repose désormais sur l'orchestration de plusieurs services souverains :
- **Podman & Podman-Compose :** Environnement d'exécution conteneurisé (alternative open-source à Docker).
- **Ollama :** Backend d'inférence local pour l'exécution des LLMs (`phi3`, `qwen2.5`, etc.).
- **Open WebUI :** Interface de management centralisée, gestion de l'historique et RAG intégré.
- **Dify :** Plateforme d'orchestration "Low-Code" pour la création d'agents autonomes, workflows complexes et gestion fine du RAG.
- **ChromaDB / PostgreSQL :** Stockage vectoriel et persistance des données applicatives.

## 🏗️ Schéma d'Architecture

Ce schéma illustre l'interaction entre les services pour la création d'agents spécialisés (Veille, Expert ISO, Analyse). 

![Architecture des Agents IA](https://kroki.io/mermaid/svg/eNplkM0KwjAMhO99isnTB8HBc1dCPBjxYDzWH5BsxhWWLVP38u6GisUX-_f7_Un62XakWWmFvT1o1QvMKQeWpLZHNn7Y3Uv4fBIdz-oD6dohf6_3oIJG-Lpi0_Br9qYPl6Yqh3mankHboR5eaIvc7vVuWAXN8eCkrl9j-Z3r_EV0v9G2S_6m_TTy732T-fze1m6Ta_lzR_8-TGO3LcEewmPXD_0e2unfomrC__wvxf-_1_d38w97yI-q)

*Note : Si le schéma ne s'affiche pas ci-dessus, assurez-vous d'activer le mode "Aperçu" (Preview) de votre éditeur (Ctrl+Shift+V dans VS Code).*

> **Visualisation :** Le schéma ci-dessus montre comment **Dify** sert de cerveau d'orchestration pour créer des agents spécialisés (Veille Tech, Expert ISO). Ces agents utilisent **Ollama** comme moteur de réflexion et accèdent au **RAG** (via ChromaDB) ou au Web via le protocole **MCP**.

## 📂 Structure du Dépôt
- `docker-compose.yaml` : Fichier de configuration pour lancer l'ensemble de la stack avec Podman.
- `volumes/` : Répertoires pour la persistance des modèles Ollama et des bases de données.
- `pre-requis.md` : Guide d'installation de Podman et configuration système.
- `presentation_3w_quebec.pptx` : Support visuel de la présentation.

## 🚀 Installation Rapide
1. Clonez le dépôt : `git clone https://github.com/SachaEmmanuelTorres/3w_quebec_2026.git`
2. Lancez l'infrastructure complète :
   ```bash
   podman-compose up -d
   ```
3. Accédez aux services :
   - **Interface Chat & RAG :** `http://localhost:3000` (Open WebUI)
   - **Création d'Agents IA :** `http://localhost:80` (Dify)

---
*Projet réalisé dans le cadre de la conférence 3W Québec à l'UQAM.*

## Architecture des Agents IA
n![Architecture des Agents IA](documentation/architecture_agents_AI.png)
![Architecture des Agents IA](documentation/architecture_agents_AI.png)
