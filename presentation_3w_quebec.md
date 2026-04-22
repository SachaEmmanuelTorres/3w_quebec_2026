### IA en local :






**Le choix du LLM :**

⇒ Hugging Face : [https://huggingface.co/](https://huggingface.co/)

privilégier trois approches :

- un modèle à jour,

- un petit modèle

- un modèle par action


**Le choix de l’outil de gestion et d’interface prompt :**


**Llama.cpp : **

**OLLAMA :**






**OpenCode :**


### Agents :



**RAG :**

### MCP


### Définition du Protocole MCP Model-Context-Protocol

Le MCP est un protocole qui permet aux développeurs d’exposer des capacités, des outils et des données aux modèles d’IA de manière structurée, sûre et autorisée.


Exemple de code : indicateur occupation disque :


***def check\_disk\_usage():  
       import shutil  
       total, used, free = shutil.disk\_usage("/")  
       return \{  
              "total": total,  
              "used": used,  
              "free": free,**  
***\}**


***from** ***mcp.server import** ***Server**  
***from** ***mcp.types import** ***Tool, Schema**  
  
***server = Server()**  
***@server.tool(  
          Tool(  
                 name="check\_disk",  
                 description="Returns disk usage stats",  
                 input\_schema=Schema(type="object", properties=\{\}),  
                 output\_schema=Schema(  
                        type="object",  
                        properties=\{  
                                 "total": \{"type": "number"\},  
                                 "used": \{"type": "number"\},  
                                 "free": \{"type": "number"\}  
                        \}  
               )  
       )   
)**  
***def** ***check\_disk\_tool(\_args):**  
            ***return** ***check\_disk\_usage()**  
***server.run()**


