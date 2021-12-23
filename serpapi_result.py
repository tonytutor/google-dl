import os, urllib.request, json # json for pretty output
from serpapi import GoogleSearch
from timeit import default_timer as timer

start = timer()

def get_google_images():
    params = {
      "api_key": os.getenv("API_KEY"),
      "engine": "google",
      "q": "pexels cat",
      "tbm": "isch"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # print(json.dumps(results['suggested_searches'], indent=2, ensure_ascii=False))
    print(json.dumps(results['images_results'], indent=2, ensure_ascii=False))

    # -----------------------
    # Downloading images

    for index, image in enumerate(results['images_results']):

        print(f'Downloading {index} image...')
        
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(image['original'], f'SerpApi_Images/original_size_img_{index}.jpg')

    end = timer()
    print(end - start)