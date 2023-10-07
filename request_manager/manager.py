from playwright.sync_api import sync_playwright, Error
from request_manager.parameters.headers import headers
from bs4 import BeautifulSoup
import requests
import re


class RequestManager(object):
    """
        Class used to send a request from a
        website link or a API endpoint and
        treat the response and the requests tries.
    """
    def __init__(self, website_link: str or None = None):
        self.homeurl = website_link
        self.params = None
        self.json_data = None
        self.cookies = None
        self.data = None
        self.headers = headers
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
        self.user_agent += 'AppleWebKit/537.36 (KHTML, like Gecko) '
        self.user_agent += 'Chrome/73.0.3683.75 Safari/537.36'
        self.possible_request_error = (requests.exceptions.ConnectTimeout,
                                        requests.exceptions.SSLError,
                                        requests.exceptions.ConnectionError,
                                        requests.exceptions.ReadTimeout)

    def send_requisitons_requests(self, base_url: str, method: str='GET', max_tries: int=5, timeout : int=10, control: int=1) -> None:
        """
            Class used to send requisitions using the library
            requests passing parameters like params and headers.

            Receive as a parameter the url that is
            going to be used to send the requisition.

            By default the method will use the method GET,
            but you can pass a specif method such as 
            POST, PUT, DELETE

        """
        tried = int()
        base_url_clean = self.http_protocol_verification(base_url)
        while True:
            if tried > max_tries:
                self.availiable = False
                self.response = None
                break
            try:
                if method == 'GET':
                    self.response = requests.get(base_url,
                                                headers=self.headers,
                                                timeout=timeout,
                                                params=self.params,
                                                json=self.json_data,
                                                cookies=self.cookies,
                                                data=self.data)
                elif method == 'POST':
                    self.response = requests.post(base_url,
                                                headers=self.headers,
                                                timeout=timeout,
                                                params=self.params,
                                                json=self.json_data,
                                                cookies=self.cookies,
                                                data=self.data)
                elif method == 'PUT':
                    self.response = requests.put(base_url,
                                                headers=self.headers,
                                                timeout=timeout,
                                                params=self.params,
                                                json=self.json_data,
                                                cookies=self.cookies,
                                                data=self.data)
                elif method == 'DEL':
                    self.response = requests.delete(base_url,
                                                headers=self.headers,
                                                timeout=timeout,
                                                params=self.params,
                                                json=self.json_data,
                                                cookies=self.cookies,
                                                data=self.data)
                if self.response and not self.response.status_code in range(500, 600):
                    self.availiable = True
                    break
                else:
                    tried += 1
            except self.possible_request_error:
                tried += 1
                print(f'Connection Error - Trying the {tried} attempt...')
                continue
        if not self.availiable:
            base_url_clean = self.http_protocol_verification(base_url, 2)
            if control > 2:
                return
            if not base_url_clean == base_url:
                self.send_requisitons_requests(base_url_clean, method, max_tries, timeout, control+1)
        try:
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except (TypeError, AttributeError):
            self.soup = None

    def send_requisitions_playwright(self, url_base: str) -> None:
        """
            Class used to send requisitions using the library
            playwright passing parameters like user agent,
            most use to avoid requisitions block.

            Receive as a parameter the url that is
            going to be used to send the requisition.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=50)
            self.page = browser.new_page(user_agent=self.user_agent)
            tried = int()
            while True:
                try:
                    self.page.goto(url_base)
                    self.content = self.page.content()
                    self.soup = BeautifulSoup(self.content, 'html.parser')
                    break
                except Error:
                    tried += 1
                    if tried > 5:
                        self.availiable = False
                        self.response = None
                        break
                    print(f'Connection Error - Trying the {tried} attempt...')
                    continue

    def http_protocol_verification(self, link: str, attempt: int=1) -> str:
        """
            Method created to check if the link url
            has the right http protocol
        """
        if len(link) > 0:
            if link[0] == '/':
                link = link[1:]
            if not 'https' in link or 'http' in link:
                link = link.replace('//', str())
                if attempt == 1:
                    link = f'https://{link}'
                else:
                    link = f'http://{link}'
            return link
        else:
            raise ValueError('Need to add a valid link')

    def clean_html_tags(self, string: str) -> None:
        """
            Method created to remove all
            html tags from a specific text
        """
        regex = re.compile(r'<[^>]+>')
        return regex.sub('', string)

    def clean_description(self, description: str) -> str:
        """
            Method used to remove all html tags
            from a specific text, and change some
            object from another language to python object
        """
        description = self.clean_html_tags(description)
        need_change = [['\\', str()], ["null", '""'], ["false", "False"],
                       ["true", "True"], ['"{', "{"],  ['}"', "}"]]
        for change in need_change:
            description = description.replace(change[0], change[1])
        description = ' '.join(word for word in description.split(' '))
        return description.strip()
