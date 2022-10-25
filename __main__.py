import requests
from bs4 import BeautifulSoup
import argparse
import os.path
import pathlib

data = []
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"
           }  

def go(url): 
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    content = soup.find(id="content")
    a_tag = content.find('a', href=True)
    first_href = a_tag['href']
    
    max = (first_href).split("/")[4]
    name = (first_href).split("/")[3]

    loop(url, name, max)


def grab(url, name, max):
    r = requests.get(url + str(max))
    soup = BeautifulSoup(r.content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get('src')
        if name in src:
            if src not in data:
                data.append(src)
            else:
                data.remove(src)
    

def loop(url, name, max):
    i = int(max)
    while i>=1:
        grab(url, name, i)
        i-=1
    makeFiles(name)


def makeFiles(name):
    npath = os.path.join(path, name)
    if not os.path.exists(npath):
        os.makedirs(npath)

    dl(data, npath)


def dl(data, dir):
    i=0
    while i < len(data):
        npath = os.path.join(dir, str(i) + ".jpg")
        img = requests.get(url=data[i], headers=headers).content
        with open(npath, "wb") as handler:
            handler.write(img)

        print(f"Downloading: %d%% [%d / %d] bytes inside {path}" % (i / len(data) * 100, i, len(data)))
        
        i+=1
    print("Done.")

        

def main(path):
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='should be "https://www.xxxxx.com/xxxxx/"')
    args = parser.parse_args()
    go(args.url)



if __name__ == "__main__":
    #User config
    path = "D:\\$Forbidden\\nice\\$\\of" #You can set your default path if you want to use the app faster. Don't forget to double '\'


    main(path)
