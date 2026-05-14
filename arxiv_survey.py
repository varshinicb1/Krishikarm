import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import time

def search_arxiv(query, max_results=100):
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    response = urllib.request.urlopen(url)
    data = response.read()
    root = ET.fromstring(data)
    
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.replace('\n', ' ').strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.replace('\n', ' ').strip()
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        papers.append({
            'title': title,
            'summary': summary,
            'published': published
        })
    return papers

queries = [
    'all:"data fusion" AND all:satellite AND all:sensor AND all:agriculture',
    'all:"remote sensing" AND all:IoT AND all:fusion',
    'all:"soil moisture" AND all:fusion AND all:satellite'
]

all_papers = []
for q in queries:
    print(f"Querying: {q}")
    papers = search_arxiv(q, max_results=40)
    all_papers.extend(papers)
    time.sleep(3) # polite delay

# deduplicate
unique_papers = {p['title']: p for p in all_papers}.values()

with open('survey_results.json', 'w') as f:
    json.dump(list(unique_papers), f, indent=2)

print(f"Fetched {len(unique_papers)} unique papers.")
