from bs4 import BeautifulSoup
import requests
import os

base_url = 'https://pantip.com'
page_url = '/tag/ปัญหาสังคม'
page_id = ''

os.makedirs(os.path.dirname('../posts.csv'), exist_ok=True)

while page_url:
    re = requests.get(base_url + page_url + page_id)
    document = re.text
    re.close()

    soup = BeautifulSoup(document, 'html.parser')

    posts = soup.find_all('div', {'class': 'post-item'})
    for post in posts:
        link_tag = post.find('div', {'class': 'post-item-title'}).find('a')
        link = base_url + link_tag['href']

        comment = post.find('div', {'class': 'post-item-status-i'})
        if comment:
            comment = comment['title'].split(' ')[0]
            if int(comment) >= 70:
                with open('../posts.csv', 'a') as f:
                    f.write(link + ',' + comment + '\n')
                print(link, comment)

    try:
        page_id = soup.find('div', {'class': 'loadmore-bar'}).find('a')['href']
        index = page_id.find('?')
        page_id = page_id[index:]
    except:
        page_url = None
