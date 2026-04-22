# Mise à jour de l'Agent RAG :
# - Intégration réelle de ChromaDB pour la recherche sémantique.
# - Utilisation du modèle d'embeddings 'mxbai-embed-large' via Ollama.
# - Utilisation de 'qwen2.5:3b' pour la synthèse finale.
# - Utilisation de 'phi3:mini' pour la réflexion.

import asyncio
import httpx
import json
import chromadb
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configuration MCP pour l'automatisation du navigateur
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-puppeteer"]
)

class AgentOrchestrator:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api"
        # Initialisation de ChromaDB (local)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="iso_standards")
        self._seed_data()

    def _seed_data(self):
        """Ajoute des données de test si la collection est vide."""
        if self.collection.count() == 0:
            print("📦 Initialisation du RAG avec les normes ISO...")
            docs = [
                "Norme ISO 2026-1 : Les rapports d'actualité doivent inclure un titre H1 et une date.",
                "Norme ISO 2026-2 : Utilisez des listes à puces pour les points clés et du gras pour les entités importantes.",
                "Norme ISO 2026-3 : La synthèse finale doit être rédigée en Markdown avec une section 'Conclusion'."
            ]
            # Pour simplifier dans ce script, on utilise l'embedding par défaut de ChromaDB 
            # (qui tourne en local via sentence-transformers si installé)
            # Sinon, on pourrait passer par Ollama pour chaque doc.
            self.collection.add(
                documents=docs,
                ids=[f"id{i}" for i in range(len(docs))]
            )

    async def get_embedding(self, text):
        """Récupère l'embedding d'un texte via Ollama (mxbai-embed-large)."""
        payload = {"model": "mxbai-embed-large", "prompt": text}
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.ollama_url}/embeddings", json=payload, timeout=60.0)
            return res.json().get("embedding")

    async def ask_llm(self, model, prompt):
        """Interroge Ollama pour la génération de texte."""
        payload = {"model": model, "prompt": prompt, "stream": False}
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.ollama_url}/generate", json=payload, timeout=60.0)
            return res.json().get("response")

    async def rag_search(self, query):
        """Recherche sémantique réelle dans ChromaDB."""
        print(f"🔍 RAG : Recherche de contexte pour '{query}'...")
        
        # On récupère l'embedding de la question via Ollama
        query_embedding = await self.get_embedding(query)
        
        # Recherche dans la collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        context = " ".join(results['documents'][0])
        print(f"📄 Contexte trouvé : {context}")
        return context

    async def run_agent(self, goal, session):
        """Boucle ReAct : Réflexion -> Action (Web) -> Enrichissement (RAG) -> Synthèse"""
        print(f"🤖 Agent activé. Objectif : {goal}")
        
        # 1. RÉFLEXION (Phi-3)
        plan_prompt = f"Tu es un agent expert. Propose un plan court pour atteindre cet objectif : {goal}. Réponds directement avec le plan."
        plan = await self.ask_llm("phi3:mini", plan_prompt)
        print(f"🤔 Pensée : {plan}")

        # 2. ACTION (Browser MCP) - Navigation vers une source d'actu
        print("🌐 Navigation vers Le Monde...")
        await session.call_tool("puppeteer_navigate", arguments={"url": "https://www.lemonde.fr"})
        page_data = await session.call_tool("puppeteer_evaluate", arguments={"script": "document.body.innerText"})
        content = page_data.content[0].text[:3000] # Limite pour le contexte LLM

        # 3. ENRICHISSEMENT (RAG) - Recherche des normes de formatage
        context = await self.rag_search("format de rapport ISO 2026")

        # 4. SYNTHÈSE (Qwen 2.5)
        final_prompt = (
            f"En utilisant les informations du Web et en respectant les normes RAG fournies, "
            f"rédige un rapport complet en Markdown.\n\n"
            f"SOURCE WEB :\n{content}\n\n"
            f"NORMES ISO (RAG) :\n{context}\n\n"
            f"OBJECTIF : {goal}"
        )
        print("✍️  Rédaction de la synthèse finale...")
        return await self.ask_llm("qwen2.5:3b", final_prompt)

async def main():
    agent = AgentOrchestrator()
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result_md = await agent.run_agent("Rapport d'actualité suivant les normes ISO", session)
            
            # Sauvegarde du résultat
            with open("rapport_agent_rag.md", "w", encoding="utf-8") as f:
                f.write(result_md)
            print("\n✅ Rapport 'rapport_agent_rag.md' généré avec succès.")

if __name__ == "__main__":
    asyncio.run(main())
