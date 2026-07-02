from duckduckgo_search import DDGS


def search_cutting_data(material, operation, tool, diameter):
    query = (
        f"{operation} {material} "
        f"{tool} {diameter} mm cutting data "
        f"Sandvik OR Guhring OR Seco OR Walter"
    )

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({
                "title": r["title"],
                "url": r["href"],
                "snippet": r["body"],
            })

    return results