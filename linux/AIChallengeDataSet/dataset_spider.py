from urllib.parse import  urlencode
import requests
base_url = "https://community.challenger.ai/api/v1/competitions/datasets/"

headers = {
    'Cookie': 'scs=enpnv9hsq96uvcdbokaoqdci5ekhi8f1; Hm_lvt_7d3b54fc4f6851194af8356d74e5b18d=1535709197; Hm_lpvt_7d3b54fc4f6851194af8356d74e5b18d=1535709197; lan=zh; uid=3tgbli7wz0x8v6zm660hiysuqgukjdin; token=%242y%2407%246u5Ypkw1gn.htEOZfP2BLOE1APJmOpdY0n90JV3FJPzLNdNuj8pre; expire=1538301212',
    'Host': 'community.challenger.ai',
    'Origin': 'https://challenger.ai',
    'Referer': 'https://challenger.ai/competition/mlsv2018',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def get_json_detals(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json = response.json()
            data = json.get('data')
            link = data.get('link')
            return link
    except Exception as e:
        print(e.args)


def main():
    download_urls = []
    download_links = open("download_links.txt", 'a+')

    for v in range(19, 101, 3):
        url = base_url + "{0}/link".format(v)
        download_url = get_json_detals(url)
        download_links.write(download_url+'\n')
        download_urls.append(download_url)
        print(download_url)

    download_links.close()
    print(len(download_urls))

if __name__ == "__main__":
    main()