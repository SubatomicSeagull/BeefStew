import discord
import wikipediaapi
import requests

query = "monkeys"
wiki = wikipediaapi.Wikipedia("BeefStew", "en")
page = wiki.page(query)
if not page.exists():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        if data["query"]["search"]:
            closest_match = data["query"]["search"][0]["title"]
            page = wiki.page(closest_match)
    except Exception as e:
        print(f"Error occurred: {e}")
        page = None

if not page.exists():
    print(f"i dont know anything about {query} :(")
else:
    print(page.summary)