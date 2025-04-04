from langchain.tools import tool

@tool
def open_website(url: str):
    """Open a given URL in browser"""
    print(f"[BROWSER] Opening {url}")
    return f"Opened {url}"

@tool
def search_on_site(query: str):
    """Search for a term on a website"""
    print(f"[BROWSER] Searching for '{query}'")
    return f"Searched for '{query}'"

@tool
def click_element(selector: str):
    """Clicks an element identified by selector"""
    print(f"[BROWSER] Clicked {selector}")
    return f"Clicked {selector}"

@tool
def extract_price():
    """Extracts price from the current page"""
    print("[BROWSER] Extracted price: ₹79,999")
    return "₹79,999"
