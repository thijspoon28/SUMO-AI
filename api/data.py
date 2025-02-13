import requests  # type: ignore


#
# OLD
#


def not_sus_request(url, headers: dict | None = None):
    url = "https://www.sumo.or.jp/EnHonbashoMain/torikumiAjax/1/1/"

    if not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.sumo.or.jp/",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest"  # Often used for AJAX requests
        }

    return requests.get(url, headers=headers)


def get_matches():
    url = "https://www.sumo.or.jp/EnHonbashoMain/torikumiAjax/1/1/"

    response = not_sus_request(url)

    try:
        data = response.json()

    except Exception:
        data = response.text
        print("WARING! COULD NOT PARSE JSON, GOT RAW TEXT")

    return data

