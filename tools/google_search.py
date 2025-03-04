from googlesearch import search
import sys

def google_search(query) -> str:
    """Perform a Google search and return results as a list of URLs.
    
    Args:
        query (str): The search query string
    """
    # Do google search and parse the results into a list of URLs
    # SearchResult(link, title, description)
    results = list(search(query, num_results=3, advanced=True))
    # print(results)
    for result in results:
        if result.description:
            return result.description + "\nsource: " + result.url
    
    return "No result found"


# if main
if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your search query: ")
    results = google_search(query)
    print(results)
