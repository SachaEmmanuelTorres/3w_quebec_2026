# Agent RAG V2 - Spécialiste Veille Technologique (3W Québec)
# Objectif : Comparer le savoir Web (Frais) et le RAG (Normes/Papiers)

import asyncio
import httpx
import json
import chromadb
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Config MCP Puppeteer
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-puppeteer"]
)

class ProfessionalAgent:
    def __init__(self):
        self.ollama_base = "http://localhost:11434/api"
        self.db = chromadb.PersistentClient(path="./chroma_v2_db")
        self.collection = self.db.get_or_create_collection("tech_watch")
        self._bootstrap_docs()

    def _bootstrap_docs(self):
        """Ajoute des connaissances sur 'Claude' et les modèles Anthropic."""
        if self.collection.count() == 0:
            print("🧠 RAG : Injection des connaissances sur Claude (Anthropic)...")
            docs = [
                "Claude 3.5 Sonnet : Modèle de pointe d'Anthropic, excellent en code et raisonnement.",
                "Claude 3 Opus : Le plus puissant de la famille 3.0, très créatif.",
                "Anthropic se concentre sur l'IA constitutionnelle (Safety first).",
                "Le format 'MCP' (Model Context Protocol) a été initié par Anthropic fin 2024."
            ]
            self.collection.add(
                documents=docs,
                ids=[f"anthropic_{i}" for i in range(len(docs))]
            )

    async def call_ollama(self, endpoint, payload):
        """Wrapper générique pour l'API Ollama."""
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(f"{self.ollama_base}/{endpoint}", json=payload, timeout=90.0)
                return res.json()
            except Exception as e:
                print(f"❌ Erreur Ollama ({endpoint}): {e}")
                return None

    async def get_embedding(self, text):
        data = await self.call_ollama("embeddings", {"model": "mxbai-embed-large", "prompt": text})
        return data.get("embedding") if data else None

    async def rag_query(self, query):
        """Recherche sémantique ciblée."""
        emb = await self.get_embedding(query)
        if not emb: return "Aucune donnée RAG disponible."
        results = self.collection.query(query_embeddings=[emb], n_results=2)
        return " | ".join(results['documents'][0])

    async def ask_llm(self, model, prompt, system="Tu es un expert en IA."):
        payload = {
            "model": model, 
            "prompt": prompt, 
            "system": system,
            "stream": False,
            "options": {"temperature": 0.3}
        }
        data = await self.call_ollama("generate", payload)
        return data.get("response") if data else "Erreur de génération."

    async def run(self, topic, session):
        print(f"\n🚀 Lancement de la veille sur : {topic}")
        
        # 1. PLANIFICATION (Phi-3)
        print("🤔 Phase 1 : Planification...")
        plan = await self.ask_llm("phi3:mini", f"Établis un plan de veille technologique pour : {topic}")
        
        # 2. RECHERCHE WEB (Puppeteer)
        print("🌐 Phase 2 : Recherche Web (Google News via Puppeteer)...")
        # On simule une recherche simple sur Le Monde pour l'exemple
        await session.call_tool("puppeteer_navigate", arguments={"url": "https://www.bing.com/news/search?q=Claude+Anthropic+AI"})
        page_content = await session.call_tool("puppeteer_evaluate", arguments={"script": "document.body.innerText"})
        web_text = page_content.content[0].text[:4000]

        # 3. RECHERCHE INTERNE (RAG)
        print("📄 Phase 3 : Consultation de la base de données interne (RAG)...")
        internal_data = await self.rag_query(topic)

        # 4. SYNTHÈSE COMPARATIVE (Qwen 2.5)
        print("✍️  Phase 4 : Rédaction de la synthèse finale...")
        final_prompt = (
            f"Sujet : {topic}\n\n"
            f"INFOS WEB RÉCENTES :\n{web_text}\n\n"
            f"SAVOIR INTERNE (RAG) :\n{internal_data}\n\n"
            f"MISSION : Fais une synthèse en Markdown. Sépare bien 'Dernières Nouvelles (Web)' "
            f"et 'Connaissances Métier (RAG)'. Termine par une recommandation stratégique."
        )
        report = await self.ask_llm("qwen2.5:3b", final_prompt)
        return report

async def main():
    agent = ProfessionalAgent()
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                report_md = await agent.run("Évolutions de Claude et d'Anthropic en 2026", session)
                
                with open("veille_claude_2026.md", "w", encoding="utf-8") as f:
                    f.write(report_md)
                print("\n✅ Veille technologique terminée. Fichier 'veille_claude_2026.md' généré.")
    except Exception as e:
        print(f"💥 Erreur fatale : {e}")

if __name__ == "__main__":
    asyncio.run(main())
