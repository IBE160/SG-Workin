
import requests
from bs4 import BeautifulSoup

url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/index.html"
print(f"Fetching {url}...")
resp = requests.get(url)
soup = BeautifulSoup(resp.content, "html.parser")

# Find "hentet fra FS"
target_text = "hentet fra FS"
element = soup.find(string=lambda t: t and target_text in t)

if element:
    parent = element.parent
    print(f"Found '{target_text}' in tag: {parent.name}")
    print(f"Classes: {parent.get('class')}")
    print(f"ID: {parent.get('id')}")
    
    # Climb up to find the container
    container = parent.find_parent("div")
    if container:
        print(f"Parent Div Classes: {container.get('class')}")
        print(f"Parent Div ID: {container.get('id')}")
else:
    print(f"Could not find '{target_text}' in HTML. It might be dynamically loaded or I missed it.")

# Check for "Oppbygging og gjennomføring"
print("\nChecking 'Oppbygging og gjennomføring' container...")
opp_header = soup.find(string="Oppbygging og gjennomføring")
if opp_header:
    p = opp_header.parent
    print(f"Found in: {p.name} (Class: {p.get('class')})")
    
    grand = p.find_parent("div", class_="term")
    if grand:
        print("✅ Found inside 'div.term'. My exclude logic should have worked?")
    else:
        print("❌ NOT inside 'div.term'. Found in:")
        print(p.find_parent("div"))

