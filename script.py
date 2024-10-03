import requests
from bs4 import BeautifulSoup
import csv

def scrape_github_trending(language='python'):
    url = f'https://github.com/trending/{language}?since=daily'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    repositories = []
    for repo in soup.select('article.Box-row'):
        name = repo.select_one('h3').text.strip().replace('\n', '').replace(' ', '')
        description = repo.select_one('p.col-9')
        description = description.text.strip() if description else "No description"
        stars = repo.select_one('span.d-inline-block.float-sm-right').text.strip()
        repositories.append([name, description, stars])
    
    return repositories

def save_to_csv(data, filename='trending_repos.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Repository', 'Description', 'Stars'])
        writer.writerows(data)

if __name__ == "__main__":
    trending_repos = scrape_github_trending()
    save_to_csv(trending_repos)
    print(f"Scraped {len(trending_repos)} trending repositories and saved to trending_repos.csv")