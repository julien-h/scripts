from requests import get
from collections import defaultdict
import requests


def update_session(selenium_driver, requests_session=None):
    """
    Transfers variables such as cookies and headers from selenium to requests' session
    """
    cookies = selenium_driver.get_cookies()
    cookies_dict = {c['name']: c['value'] for c in cookies}  
    user_agent = selenium_driver.execute_script("return navigator.userAgent;")
    referer = selenium_driver.current_url

    s = requests_session or requests.Session()
    s.cookies.update(cookies_dict)
    s.headers.update({'user-agent': user_agent})
    s.headers.update({'referer': referer})
    return s


def download(selenium_driver, url, filename, save_cookies=True):
    """
    Downloads `url` into `filename`. The download is executed through the requests library.
    Variables (cookies, user-agent, referer) are transfered from selenium to requests.
    If the download set cookies and `save_cookies==True`, then the new cookies are added
    to selenium session. The value of the referer variable is selenium's current_url.
    """
    s = update_session(selenium_driver)

    with s.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.writelines(r)
        if not save_cookies:
            return
        for c in r.cookies:
            d = to_cookie_dict(c)
            selenium_driver.add_cookie(d)
    return None


def to_cookie_dict(requests_cookie):
    """
    Transforms a requests' cookie jar into a dict that can be used by selenium
    """
    c = requests_cookie
    res = {'name': c.name, 'value': c.value, 'expiry': c.expires}
    if c.path_specified:
        res['path'] = c.path
    if c.port_specified:
        res['port'] = c.port
    return res


def update_driver(requests_session, selenium_driver):
    """
    This one is not very robust due to selenium's limitations...
    https://stackoverflow.com/questions/37490665/python-requests-cookies-export-to-selenium
    """
    cookies = defaultdict(list)
    for c in requests_session.cookies:
        domain = 'http://' + c.domain.lstrip('.')
        cookies[domain].append(to_cookie_dict(c))

    for domain, cs in cookies:
        selenium_driver.get(domain)
        for c in cs:
            selenium_driver.add_cookie(c)
    return None

