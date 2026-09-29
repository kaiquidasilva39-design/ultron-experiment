from app.research import research

url = "https://example.com"

result = research(url)

print("Pesquisa funcionando")
print("URL:", result["url"])
print("Caracteres:", result["length"])
print(result["text"][:300])
