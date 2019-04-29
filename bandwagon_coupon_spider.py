import requests
from bs4 import BeautifulSoup
import time
import re
import json


def get_discount(promocode):
    data = {'promocode': promocode}
    res = re.search(r'- ([\d\.]+)%', requests.post('https://bwh88.net/cart.php?a=view', data).text)
    if res:
        return res.group(1)
    return False


def get_promo_code(old):
    resp = requests.get('https://bwh88.net/vps-hosting.php')
    bs4obj = BeautifulSoup(resp.text, "html.parser")
    urls = []
    for vps in bs4obj.find_all('div', class_='bronze'):
        urls.append(vps.find('a')['href'])
    promo_codes = []
    for url in set(urls):
        resp = requests.get('https://bwh88.net/' + url)
        code = re.search(r'Try this promo code: (\w*)', resp.text)
        p_code = code.group(1)
        if p_code in old:
            print('dup =>', p_code)
            continue
        p_dis = get_discount(p_code)
        if p_dis:
            old.append(p_code)
            print(p_code, p_dis + '%')
            promo_codes.append((p_code, p_dis))
    return promo_codes


old = []
res = []
while 1:
    codes = get_promo_code(old)
    if codes:
        res += codes
    else:
        break

print('------ Coupons ------')
for c in res:
    print(c[0], c[1] + '%')
