
#L'utilisation de Small Language Models (SLM) transformés en "spécialistes" permet d'optimiser les ressources de votre machine locale en réduisant drastiquement l'occupation de la RAM et du #CPU [1][3]. Plutôt qu'un modèle généraliste lourd, cette architecture distribue la charge de travail sur trois modèles légers et agiles [5] :

#Extraction et Navigation (Hermes-3-Llama-3.2-3B) : Ce modèle est optimisé pour le Function Calling, permettant d'activer les outils du serveur MCP avec précision [3].

#Résumé et Analyse (Phi-3.5 Mini) : Très rapide, il traite efficacement de longs contextes textuels extraits du web pour en extraire l'essentiel [1].

#Formatage (Mistral 7B) : Utilisé spécifiquement pour ses capacités rédactionnelles supérieures en Markdown [3].

#Cette approche garantit une meilleure fluidité sur votre système Ubuntu tout en évitant la saturation de la mémoire vive [4][6].


"""
PRÉREQUIS SPÉCIFIQUES SUPPLÉMENTAIRES :
1. Modèles Ollama installés : 
   - `ollama pull hermes3` (Navigation/Outils)
   - `ollama pull phi3:mini` (Résumé)
   - `ollama pull mistral` (Rédaction)
2. Bibliothèque 'httpx' installée : `pip install httpx`
"""

import asyncio
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configuration du serveur MCP Puppeteer
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-puppeteer"]
)

class LocalAIOrchestrator:
    def __init__(self, base_url="http://localhost:11434/api/generate"):
        self.base_url = base_url

    async def call_local_llm(self, model_name, prompt):
        """Appel générique à Ollama"""
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, timeout=60.0)
            return response.json().get("response")

async def main():
    ai = LocalAIOrchestrator()
    url = "https://www.lemonde.fr"
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # ÉTAPE 1 : Navigation via MCP
            print(f"🚀 Navigation vers {url}...")
            await session.call_tool("puppeteer_navigate", arguments={"url": url})
            
            # ÉTAPE 2 : Extraction
            result = await session.call_tool(
                "puppeteer_evaluate", 
                arguments={"script": "document.body.innerText"}
            )
            raw_content = result.content[0].text[:4000]

            # ÉTAPE 3 : Résumé (Phi-3-Mini)
            print("🧠 Résumé en cours avec Phi-3-Mini...")
            prompt_resume = f"Résume les points clés :\n\n{raw_content}"
            summary = await ai.call_local_llm("phi3:mini", prompt_resume)

            # ÉTAPE 4 : Mise en forme (Mistral)
            print("📝 Mise en forme Markdown avec Mistral...")
            prompt_md = f"Transforme en Markdown élégant :\n\n{summary}"
            final_md = await ai.call_local_llm("mistral", prompt_md)

            # ÉTAPE 5 : Sauvegarde
            with open("compte_rendu.md", "w", encoding="utf-8") as f:
                f.write(final_md)
            
            print("✅ Opération terminée : 'compte_rendu.md' généré.")

if __name__ == "__main__":
    asyncio.run(main())

