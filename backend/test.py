from requests_html import HTMLSession
import requests
import http.client


def not_sus_request(url, headers: dict | None = None):
    url = "https://www.sumo.or.jp/EnHonbashoMain/hoshitori/1/1/"

    if not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.sumo.or.jp/",
            "Accept-Language": "en-US,en;q=0.9",
            "X-Requested-With": "XMLHttpRequest"  # Often used for AJAX requests
        }

    return requests.get(url, headers=headers)

# print(not_sus_request("").text)

def curl(url: str, path: str):
    conn = http.client.HTTPSConnection(url)  # Only pass the domain name
    conn.request("GET", path)  # Pass the path separately
    response = conn.getresponse()

    data = response.read().decode()  # Read and decode the response
    conn.close()

    return data  # Return the response instead of printing it


base_url = "https://www.sumo.or.jp"

def get_img_url(rikishi_id: int):
    session = HTMLSession()
    url = f"{base_url}/EnSumoDataRikishi/profile/{rikishi_id}/"
    response = session.get(url)

    # Use CSS selectors to find elements
    # title = response.html.find('title', first=True).text
    # print("Title:", title)

    # Find all links with a specific class
    links = response.html.find('img.col1')
    for link in links:
        return base_url + link.attrs['src'] 
    
    return None


print(get_img_url(3548))

