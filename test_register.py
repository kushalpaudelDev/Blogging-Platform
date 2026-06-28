import urllib.request
import urllib.parse
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

# GET register to get csrf
req = urllib.request.Request("http://127.0.0.1:8003/register/")
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8')
import re
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
if csrf:
    csrf = csrf.group(1)
    print("Found CSRF")

