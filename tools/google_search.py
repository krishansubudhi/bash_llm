from googlesearch import search
import sys
from typing import List


def google_search(query: str) -> str:
    """Perform a Google search and return formatted results.
    
    Args:
        query (str): The search query string
        
    Returns:
        str: Formatted search results with title, description, and source URL
    """
    # Perform search with advanced results
    results = list(search(query, num_results=3, advanced=True))
    
    if not results:
        return "No results found"
    
    # Format each result with markdown-style formatting
    formatted_results = []
    for result in results:
        if result.description:
            formatted_result = (
                f"### {result.title}\n"
                f"{result.description}\n"
                f"**Source:** {result.url}\n"
                "---\n"
            )
            formatted_results.append(formatted_result)
    
    return "\n".join(formatted_results) if formatted_results else "No results found"


if __name__ == "__main__":
    # Get query from command line args or user input
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your search query: ")
    print(f"\nSearching for: {query}\n")
    
    # Perform search and display results
    results = google_search(query)
    print(results)
