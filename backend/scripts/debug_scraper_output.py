
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/index.html"
print(f"Fetching {url}...")
resp = requests.get(url)
soup = BeautifulSoup(resp.content, "html.parser")

html_content = str(soup)
match = re.search(r'(.{100})hentet fra FS(.{100})', html_content, re.DOTALL | re.IGNORECASE)

if match:
    print("\n✅ Found 'hentet fra FS' in raw HTML!")
    print(f"Context:\n...{match.group(1)} >>hentet fra FS<< {match.group(2)}...")
else:
    print("\n❌ 'hentet fra FS' NOT found in raw HTML.")
