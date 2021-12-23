from timeit import default_timer as timer
import requests, lxml, re, json
from bs4 import BeautifulSoup

start = timer()

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

params = {
    "q": "minecraft shaders 8k photo",
    "tbm": "isch",
    "ijn": "0",
}

html = requests.get("https://www.google.com/search", params=params, headers=headers)
soup = BeautifulSoup(html.text, 'lxml')


def get_suggested_search_data():

    for suggested_search in soup.select('.PKhmud.sc-it.tzVsfd'):
        suggested_search_name = suggested_search.select_one('.hIOe2').text
        suggested_search_link = f"https://www.google.com{suggested_search.a['href']}"

        # https://regex101.com/r/y51ZoC/1
        suggested_search_chips = ''.join(re.findall(r'=isch&chips=(.*?)&hl=en-US', suggested_search_link))
        print(f"{suggested_search_name}\n{suggested_search_link}\n{suggested_search_chips}\n")

    # this steps could be refactored to a more compact
    all_script_tags = soup.select('script')

    # https://regex101.com/r/48UZhY/6
    matched_images_data = ''.join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
    
    # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # if you try to json.loads() without json.dumps it will throw an error:
    # "Expecting property name enclosed in double quotes"
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # search for only suggested search thumbnails related
    # https://regex101.com/r/ITluak/2
    suggested_search_thumbnails_data = ','.join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))

    # https://regex101.com/r/MyNLUk/1
    suggested_search_thumbnail_links_not_fixed = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails_data)

    print('Suggested Search Thumbnails:')  # in order
    for suggested_search_fixed_thumbnail in suggested_search_thumbnail_links_not_fixed:
        # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
        suggested_search_thumbnail = bytes(suggested_search_fixed_thumbnail, 'ascii').decode('unicode-escape')
        print(suggested_search_thumbnail)

    end = timer()
    print(end - start)