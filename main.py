
'''
Grab Record repo download stats from the Docker Registry every minute.
'''

from bs4 import BeautifulSoup
import os
import requests
from requests.exceptions import ConnectionError
from socket import error as SocketError
import time
from time import localtime, strftime


basedir = os.path.abspath(os.path.dirname(__file__))
OUTFILE = os.path.join(basedir, 'stats.csv')


def append_result(res):
    '''Append a single result to the file in csv format'''
    tm = time.time()
    with open(OUTFILE, 'a') as f:
        f.write('{},{}\n'.format(tm, res))


def scrape():
    try:
        r = requests.get('https://registry.hub.docker.com/search?q=dockerui')
    except (SocketError, ConnectionError):
        return
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text)
    
    repos = soup.find_all('div', class_='span9')[1].find_all('a')

    # The most popular is dockerui/dockerui
    for repo in repos:
        if repo['href'] == '/u/dockerui/dockerui/':
            dockerui = repo
    
    # Find count, append result to file.
    count = dockerui.find('div', class_='repo-list-item-stats-right').find('div').text

    print('Time: {} Count: {}'.format(strftime("%a, %d %b %Y %X +0000", localtime()), count))
    append_result(count)


if __name__ == '__main__':
    while True:
        scrape()
        time.sleep(60)
