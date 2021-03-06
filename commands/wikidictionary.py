import requests as http

# Szuka artykułów na Wikipedii.
def search(key, limit=10):
    key = key.replace(" ", "_")
    request = http.get(f"https://pl.wiktionary.org/w/rest.php/v1/search/page?q={key}&limit={limit}")
    results = []

    # Przygotowuje wyniki.
    for x in request.json()["pages"]:
        if x['thumbnail'] is not None:
            image = x['thumbnail']['url']
        else:
            image = ""
        result = {"Tytuł": x['title'],
                  "Opis": x['description'],
                  "URL": f"https://pl.wiktionary.org/wiki/{key}",
                  "Obrazek": image}
        results.append(result)
    return results


# Pokazuje artykuł.
def show(key):
    key = key.replace(" ", "_")
    summary = http.get(f"https://pl.wiktionary.org/api/rest_v1/page/summary/{key}")

    # Sprawdza czy istnieje.
    if summary.status_code == 404:
        return None

    # Przygotowanie strony
    summary = summary.json()

    extract = http.get(f"https://pl.wiktionary.org/w/api.php?format=json&action=query&prop=extracts"
                       f"&exintro&explaintext&redirects=1&pageids={summary['pageid']}")
    extract = extract.json()

    try:
        image = summary['thumbnail']['source']
    except KeyError:
        image = None

    page = {"Tytuł": summary['displaytitle'],
            "Obrazek": image,
            "Opis": extract['query']['pages'][f"{summary['pageid']}"]['extract'],
            "URL": summary['content_urls']['desktop']['page']}
    return page
