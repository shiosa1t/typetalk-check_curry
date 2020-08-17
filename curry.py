import pycurl
import json
from io import BytesIO
from PIL import Image, ImageOps
import requests
import cloudinary
import cloudinary.uploader
import pycurl
import time
import threading

url = ""
token = ""
bot = ""

cloudinary.config(
  cloud_name = "",
  api_key = "",
  api_secret = ""
)

python3 = False
try:
    from StringIO import StringIO
except ImportError:
    python3 = True
    import io as bytesIOModule
from bs4 import BeautifulSoup
if python3:
    import certifi

def reverse_search(image_url):
    """Returns reverse image search results from url"""
    return parseResults(doImageSearch(image_url))


def doImageSearch(image_url):
    """Perform the image search and return the HTML page response."""

    if python3:
        returned_code = bytesIOModule.BytesIO()
    else:
        returned_code = StringIO()
    full_url = SEARCH_URL + image_url


    conn = pycurl.Curl()
    if python3:
        conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11")
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    if python3:
        return returned_code.getvalue().decode("UTF-8")
    else:
        return returned_code.getvalue()

def parseResults(code):
    """Parse/Scrape the HTML code for the info we want."""

    soup = BeautifulSoup(code, "html.parser")
    check = str(soup.find("div", attrs={"class":"a4bIc"}))
    num = (check.find("input", 50))
    scope = check[num-1:-8]+">"
    edit = BeautifulSoup(scope, "html.parser")
    result = edit.find("input", {"name": "q"})["value"]
    return result

SEARCH_URL = "https://www.google.com/searchbyimage?&image_url="
headers = {"X-TYPETALK-TOKEN": token}

def curry():
    r = requests.get(url, headers=headers)
    print(r.status_code)
    dic = json.loads(r.text)
    l = len(dic["posts"])
    i = 0
    while True:
        if i == l:
            break;
        elif dic["posts"][i]["attachments"]:
            m = len(dic["posts"][i]["likes"])
            j = 0
            while True:
                if j == m:
                    img_url = dic["posts"][i]["attachments"][0]["apiUrl"]
                    img_type = dic["posts"][i]["attachments"][0]["attachment"]["contentType"][6:]
                    img_r = requests.get(img_url, headers=headers)
                    img = Image.open(BytesIO(img_r.content))
                    img_name = "curry." + img_type
                    img.save(img_name)
                    cloud = cloudinary.uploader.upload(file=img_name)
                    result = reverse_search(cloud["secure_url"])
                    if "curry" in result or "カレー" in result:
                        msg = "カレー！"
                    else:
                        msg = "カレーじゃない..."
                    data = {"message":msg+"\n("+result+")", "replyTo":dic["posts"][i]["id"]}
                    like = url + "/posts/{id}/like".format(id=dic["posts"][i]["id"])
                    requests.post(like, headers=headers)
                    requests.post(url, json=data, headers=headers)
                    print("Image was detected!")
                    i+=1
                    break;
                elif dic["posts"][i]["likes"][j]["account"]["name"] == bot:
                    i+=1
                    break;
                else:
                    j+=1
        else:
            i+=1

def scheduler(interval, f, wait = True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

scheduler(60, curry, False)