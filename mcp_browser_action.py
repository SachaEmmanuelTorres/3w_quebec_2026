import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configuration du serveur MCP Web Browser
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-puppeteer"],
    env=None
)

async def main():
    url_to_visit = "https://www.example.com"
    output_file = "resume_page.md"

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(f"🌐 Navigation vers : {url_to_visit}...")
            
            await session.call_tool("puppeteer_navigate", arguments={"url": url_to_visit})

            result = await session.call_tool(
                "puppeteer_evaluate", 
                arguments={"script": "document.body.innerText"}
            )
            raw_text = result.content[0].text

            print("📝 Analyse et résumé du contenu...")
            resume = simuler_resume_llm(raw_text)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Résumé de la page : {url_to_visit}\n\n")
                f.write(f"## Contenu synthétisé\n\n{resume}\n\n")
                f.write("---\n*Généré automatiquement via MCP & Python*")

            print(f"✅ Document sauvegardé sous : {output_file}")

def simuler_resume_llm(texte):
    """Simule l'appel à un serveur local Ollama."""
    debut_texte = texte[:500].replace('\n', ' ')
    return f"Résumé automatique :\n- {debut_texte}..."

if __name__ == "__main__":
    asyncio.run(main())
