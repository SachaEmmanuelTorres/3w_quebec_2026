### IA en local : Optimisation et Orchestration

**Le choix du LLM :**
⇒ Hugging Face : [https://huggingface.co/](https://huggingface.co/)

Approche structurée :
- **Modèles optimisés pour le code :** Granite 3.0 3B (Instruct) et Qwen 2.5 3B (Instruct, version Q6_K).
- **Format :** Utilisation systématique du format GGUF pour la compatibilité native.

**Le choix des outils de gestion et d'interface :**

*   **Llama.cpp :** Serveur backend haute performance pour les modèles GGUF.
*   **Ollama :** Gestionnaire de modèles local optimisé, intégré avec Open-WebUI.
*   **OpenCode-GUI :** Environnement de développement complet conteneurisé.
*   **OpenRouter-Proxy (LiteLLM) :** Hub central pour l'orchestration des modèles.

---

### Agents :

*   **RAG (Retrieval Augmented Generation) :** Système basé sur Marimo pour interroger dynamiquement vos connaissances locales.
*   **Interfaces graphiques :** Open-WebUI (Port 3000) et Chatbot UI (Port 3001).

---

### MCP (Model Context Protocol) - Partie 1

**Définition :**
Le MCP est un protocole standardisé permettant d'exposer des capacités, des outils et des données aux modèles d'IA de manière structurée et sécurisée.

**Exemple de code (outil MCP - Partie 1) :**

```python
def check_disk_usage():
    import shutil
    total, used, free = shutil.disk_usage("/")
    return {
        "total": total,
        "used": used,
        "free": free
    }

from mcp.server import Server
from mcp.types import Tool, Schema
```

---

### MCP (Model Context Protocol) - Partie 2

**Exemple de code (outil MCP - Partie 2) :**

```python
server = Server()
@server.tool(
    Tool(
        name="check_disk",
        description="Returns disk usage stats",
        input_schema=Schema(type="object", properties={}),
        output_schema=Schema(
            type="object",
            properties={
                "total": {"type": "number"},
                "used": {"type": "number"},
                "free": {"type": "number"}
            }
        )
    )
)
def check_disk_tool(_args):
    return check_disk_usage()

server.run()
```
