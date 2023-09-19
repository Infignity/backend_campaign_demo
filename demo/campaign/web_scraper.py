import trafilatura
import os
# import logging
import requests
from .data import login_headers, extension_headers


def scrape_website(url):
    ''' scrapping web pages using the url parameter'''
    # try:
    # Fetch the HTML content from the URL
    html_content = trafilatura.fetch_url(url)
    # Parse the HTML content and extract structured data
    data = trafilatura.extract(
        html_content,
        include_links=True,
        # output_format='xml',
        include_tables=True,
        url=url
        )

    # print data
    print(data)

    return data
    # except Exception as exception:
    #     print(f"Error: {str(exception)}")
    #     return None
    

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
        return apolo_request_sesion(linkedin_url)
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
         'https://app.apollo.io/api/v1/contacts',
         headers=extension_headers,
         json=json_data
        )
    
    if res.status_code != 200:
        print("Contact apollo request failed, ", res.text)
        # repeated_attempts += 1
        apolo_request_sesion(linkedin_url)
        # continue

    data = res.json()
    if data.get('contact') == {}:
        print('Not a person data, ', data)
        apolo_request_sesion(linkedin_url)
        # row = next(reader, None)
        # continue
    return data
