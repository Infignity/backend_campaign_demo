# importing packages
import os
import re
import trafilatura
import requests
from bs4 import BeautifulSoup
from .data import login_headers, extension_headers, cookies, headers


class WebScrapping:
    '''web scrapping function'''

    @staticmethod
    def scrape_website(url):
        ''' scrapping web pages using the url parameter'''
        html_content = trafilatura.fetch_url(url)
        # Parse the HTML content and extract structured data
        data = trafilatura.extract(
            html_content,
            include_links=True,
            # output_format='xml',
            include_tables=True,
            url=url
        )
        return data

    @staticmethod
    def get_url_website(website_url):
        '''get all the urls on the companies website'''
        resp = requests.get(url=f'https://{website_url}').text

        soup = BeautifulSoup(resp, 'html.parser')
        # extract the links
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href')]

    @staticmethod
    def get_all_content(urls):
        """get website urls context data"""
        content = []
        for url in urls:
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find and remove all anchor link tags
                for anchor in soup.find_all('a'):
                    anchor.extract()
                # Extract the remaining text
                text_content = soup.get_text().replace('\n', "")
                content.append(text_content)
            else:
                print("Failed to retrieve the web page")
        return content

    @staticmethod
    def is_domain_url(url, domain):
        '''match pattern'''
        domain_pattern = re.compile(r'https?://([a-zA-Z0-9.-]*\.)?' + domain)
        return domain_pattern.search(url) is not None
    
    @staticmethod
    def domain_related_route(urls, target_domain):
        '''get webpages on same domain'''
        domain_urls = [
            url for url in urls if WebScrapping.is_domain_url(
                url, target_domain)]
        return domain_urls[:10]
        
    @staticmethod
    def apolo_request_sesion(linkedin_url):
        '''use appollo to get company informations'''
        req_session = requests.Session()
        username = os.environ.get('APOLO_USERNAME')
        password = os.environ.get('APOLO_PASSWORD')

        json_data = {
            'email': username,
            'password': password,
            'timezone_offset': -240,
        }
        response = req_session.post(
            'https://app.apollo.io/api/v1/auth/login',
            headers=login_headers,
            json=json_data
        )
        if response.status_code != 200:
            print('login failed', username, password)
            return WebScrapping.apolo_request_sesion(linkedin_url)
        print('logged in successfully')

        json_data = {
            'linkedin_url': f'{linkedin_url}',
            'contact_stage': {
                'id': None,
                'name': 'No Stage',
            },
            'account_phone_number': {
                'status': 'no_status',
                'type': 'work_hq_account',
            },
            "email_status": "verified",
            "email_source": "microsoft_login_tickle",
            "existence_level": "none",
            "typed_custom_fields": {},
            "email_true_status": "Unavailable",
            "updated_email_true_status": True,
            "source": "chrome_extension_linkedin",
        }
        res = req_session.post(
            os.environ.get('APOLO_CONTACT'),
            headers=extension_headers,
            json=json_data
        )
        if res.status_code != 200:
            print("Contact apollo request failed, ", res.text)
            # repeated_attempts += 1
            WebScrapping.apolo_request_sesion(linkedin_url)
            # continue

        data = res.json()
        if data.get('contact') == {}:
            print('Not a person data, ', data)
            WebScrapping.apolo_request_sesion(linkedin_url)
        return data


class ApolloCompany:
    ''' using apollo to get company data'''

    def __init__(self, website_url):
        self.domain = self.clean_url(website_url)

    def clean_url(self, url):
        '''clean the url link'''
        clean_url_match = re.search(
            r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', url)
        return re.sub(r'https?:\/\/', '', clean_url_match.group())

    def search_company(self):
        '''search company'''
        company_domain = self.domain
        json_data = {
            'q_organization_fuzzy_name': company_domain.strip(),
            'display_mode': 'fuzzy_select_mode',
            'cacheKey': os.environ.get('COMPANY_COOKIES_KEY'),
        }
        response = requests.post(
            os.environ.get('APOLO_SEARCH'),
            cookies=cookies,
            headers=headers,
            json=json_data
        )
        results = response.json()['organizations']

        if len(results) == 0:
            return None
        return results[0]

    def get_data(self):
        '''get the company data'''
        org = self.search_company()
        if org is None:
            return None
        org_id = org['id']
        req = requests.get(
            f"{os.environ.get('APOLO_URL')}{org_id}",
            cookies=cookies,
            headers=headers
        )
        return req.json()
