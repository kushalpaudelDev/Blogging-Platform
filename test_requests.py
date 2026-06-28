import urllib.request
import urllib.error

def check_url(url):
    try:
        urllib.request.urlopen(url)
        print(f"{url} OK")
    except urllib.error.HTTPError as e:
        print(f"{url} Error: {e.code} - {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"{url} Error: {e}")

check_url("http://127.0.0.1:8000/")
check_url("http://127.0.0.1:8000/login/")
check_url("http://127.0.0.1:8000/register/")
