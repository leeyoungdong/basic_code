import requests
from requests.exceptions import RequestException
import urllib.parse

from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper

import psycopg2

class SingletonMeta(type):
    """Singleton 메타클래스.
    
    이 클래스는 Singleton 패턴을 구현하는 데 사용되는 메타클래스입니다.
    클래스의 인스턴스가 생성되었는지 확인하고 없으면 생성, 있으면 반환합니다.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """인스턴스 생성 또는 반환."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class HttpRequestHandler:
    """HTTP 요청 핸들러.
    
    주어진 URL과 헤더를 사용하여 웹 페이지를 가져옵니다.
    """
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {}
        self.response = self._get_web_page()
        
    def _get_web_page(self):
        """웹 페이지 가져오기.
        
        주어진 URL로 HTTP GET 요청을 보냅니다. 오류가 발생하면 인증서를 검증하지 않는 방식으로 재시도합니다.
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException:
            response = requests.get(self.url, headers=self.headers, verify=False)
            response.raise_for_status()

        return response

    def json_content(self):
        """JSON 내용 반환.
        
        응답의 content-type 헤더가 'application/json'인 경우 JSON 내용을 반환합니다.
        """
        return self.response.json() if self.response.headers.get('content-type') == 'application/json' else None

    def download_file(self, save_path):
        """응답 내용을 파일로 다운로드.
        
        인자:
        - save_path: 저장할 파일의 경로.
        """
        with open(save_path, 'wb') as file:
            file.write(self.response.content)
        print(f"File saved to {save_path}")

class SessionRequestHandler:
    """세션을 유지하며 HTTP 요청을 처리하는 핸들러.
    """
    def __init__(self, login_url, headers=None, payload=None):
        """
        생성자 메서드.
        
        인자:
        - login_url: 로그인 URL.
        - headers: HTTP 헤더.
        - payload: 로그인에 사용할 데이터.
        """
        self.login_url = login_url
        self.headers = headers or {}
        self.payload = payload or {}
        self.session = requests.Session()
        
    def __enter__(self):
        """
        컨텍스트 관리자 진입 메서드.
        
        로그인을 수행하고, 로그인에 실패하면 예외를 발생시킵니다.
        """
        response = self.session.post(self.login_url, headers=self.headers, data=self.payload)
        response.raise_for_status()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        컨텍스트 관리자 종료 메서드.
        
        세션을 종료합니다.
        """ 
        self.session.close()
        
    def download_file(self, url, save_path):
        """
        세션을 사용하여 파일 다운로드.
        
        인자:
        - url: 다운로드할 파일의 URL.
        - save_path: 저장할 파일의 경로.
        
        파일을 성공적으로 다운로드하면 파일 경로를 출력하고, 
        다운로드에 실패하면 에러 메시지를 출력합니다.
        """
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            content_type = response.headers.get('content-type', '')
            with open(save_path, 'wb') as file:
                file.write(response.content)

        except RequestException as e:
            print(f"Error downloading file: {e}")

class PostgresHandler:
    """PostgreSQL 핸들러.
    
    PostgreSQL 데이터베이스와의 연결 및 쿼리 실행을 관리합니다.
    """
    def __init__(self, dbname, user, password, host, port=5432):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, data=None):
        """쿼리 실행 및 커밋."""
        self.cursor.execute(query, data)
        self.connection.commit()

    def close(self):
        """데이터베이스 연결 종료."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


class JsonHandler:
    """JSON 데이터 핸들러.
    
    JSON 형식의 데이터를 저장하고, 특정 키를 통해 데이터를 가져오는 기능을 제공합니다.
    """
    def __init__(self):
        self.json_data = {}

    def data_to_json(self, data):
        """데이터를 JSON 형식으로 변환하여 저장.
        
        인자:
        - data: 저장할 데이터
        """
        for idx, item in enumerate(data):
            self.json_data[f'key_{idx}'] = item

    def get_data_from_json_key(self, key):
        """키를 이용해 JSON 데이터에서 값을 가져옵니다.
        
        인자:
        - key: 검색할 키 값
        """
        return self.json_data.get(key, None)


class BaseScraper:
    """웹 스크랩핑 기본 클래스.
    
    웹 페이지의 데이터를 가져와서 PostgreSQL 데이터베이스에 저장합니다.
    """
    def __init__(self, url, headers=None, dbname="", user="", password="", host="", port=""):
        self.http_request = HttpRequestHandler(url, headers)
        if dbname and user and password and host and port:
            self.db_handler = PostgresHandler(dbname, user, password, host, port)
        self.json_handler = JsonHandler()

        
    def get_data_from_keys(self, *keys):
        """키를 사용하여 데이터 가져오기."""
        data = self.json_handler.json_data
        for key in keys:
            data = data.get(key)
            if data is None:
                return None
        return data

    def save_data_to_db(self, data, table_name):
        """주어진 데이터를 데이터베이스에 저장.
        
        인자:
        - data: 데이터
        - table_name: 테이블명
        """

        for item in data:
            query = f"INSERT INTO {table_name} (data) VALUES (%s);"
            self.db_handler.execute_query(query, (item,))
        self.db_handler.close()

class CloudBs4Scraper(BaseScraper, metaclass=SingletonMeta):
    """Beautiful Soup 4를 클라우드 사용하는 스크래퍼.
    
    HTML 콘텐츠에서 데이터를 추출하기 위해 BeautifulSoup 4 라이브러리를 사용합니다.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scraper = cloudscraper.create_scraper()
        self.fetch_content(self.url) 

    @staticmethod
    def fetch_content(url):
        """URL로부터 HTML 콘텐츠를 가져와서 soup 객체를 생성합니다."""
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status() 
        return response.content

class Bs4Scraper(BaseScraper, metaclass=SingletonMeta):
    """Beautiful Soup 4를 사용하는 스크래퍼.
    
    HTML 콘텐츠에서 데이터를 추출하기 위해 BeautifulSoup 4 라이브러리를 사용합니다.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = BeautifulSoup(self.http_request.response.content, 'html.parser')

    def get_data(self, selectors):
        """CSS 선택자를 사용하여 데이터를 가져옵니다.
        
        인자:
        - selectors: CSS 선택자 리스트
        """
        if not isinstance(selectors, list):
            selectors = [selectors]
        return [[item.text for item in self.soup.select(selector)] for selector in selectors]

class LxmlScraper(BaseScraper, metaclass=SingletonMeta):
    """lxml을 사용하는 스크래퍼.
    
    HTML/XML 콘텐츠에서 데이터를 추출하기 위해 lxml 라이브러리를 사용합니다.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = etree.HTML(self.http_request.content)

    def get_data(self, xpaths):
        """XPath를 사용하여 데이터를 가져옵니다.
        
        인자:
        - xpaths: XPath 리스트
        """
        if not isinstance(xpaths, list):
            xpaths = [xpaths]
        return [[item.text if hasattr(item, 'text') else item for item in self.tree.xpath(xpath)] for xpath in xpaths]


class OpenApiHandler(BaseScraper, metaclass=SingletonMeta):
    """Open API 핸들러.
    
    Open API의 데이터를 가져오고 JSON 형식으로 저장합니다.
    """
    def __init__(self, api_base_url, api_key=None, headers=None, dbname="", user="", password="", host="", port=5432):
        self.http_request = HttpRequestHandler(api_base_url, headers)
        self.json_handler = JsonHandler()
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.headers = headers

        if dbname and user and password and host and port:
            self.db_handler = PostgresHandler(dbname, user, password, host, port)

    def get_endpoint_data(self, endpoint="", params=None):
        """API 엔드포인트에서 데이터를 가져옵니다.
        
        인자:
        - endpoint: API 엔드포인트
        - params: 요청에 전달할 파라미터
        """
        params = params or {}
        if self.api_key:
            params['api_key'] = self.api_key
        full_url = urllib.parse.urljoin(self.api_base_url, endpoint)
        response = requests.get(full_url, headers=self.headers, params=params)
        if response.status_code == 200:
            self.json_handler.data_to_json(response.json())
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

if __name__ == '__main__':
    print(".py file execute")
