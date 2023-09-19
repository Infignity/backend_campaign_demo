# APOLLO ENRICHMENT
# Use Linkedin URL to find the id and use Apollo Api to find the email
# The id is from apollo chrome extension endpoint.
# 
# NOTE: 1. Not using proxies
#       2. Enriching one id at a time
#       3. Account is changed only when request does not suceed


import requests
import logging
import csv
import random
import pandas as pd
from data import login_headers, extension_headers, frontend_headers


def enrich():
    
    # TEST config
    linkedin_column_name = 'Linkedin'

    csvpath = "test.csv" # TODO: change the path
    csvfile = open(csvpath, encoding='utf-8')
    reader = csv.DictReader(csvfile)

    
    def get_apollo_session():
        with open('accounts.txt') as f:
            accounts = [i.split(", ") for i in f.readlines()]
            account = random.choice(accounts)
            username = account[0]
            password = account[1]

        s = requests.Session()
        username = "laura@monday2.cloud"
        password = "Magicpitch1*"

        json_data = {
            'email': username,
            'password': password,
            'timezone_offset': -240,
        }
        response = s.post('https://app.apollo.io/api/v1/auth/login',
                   headers=login_headers, 
                   json=json_data)
        
        if response.status_code != 200:
            logging.warning('login failed', username, password)
            return get_apollo_session()
        
        logging.info('logged in successfully')

        return s
    
    
    s = get_apollo_session()
    row = next(reader)
    repeated_attempts = 0
    final_data = []
    i = 0
    while True:
        if row is None:
            break

        if repeated_attempts > 5:
            logging.error("Enrichment not working")
            raise Exception('Enrichment not working.')

        linkedin_username = row[linkedin_column_name].replace('http://www.linkedin.com/in/', '')
        
        if linkedin_username == '':
            row = next(reader, None)
            continue

        json_data = {
            'linkedin_url': f'http://www.linkedin.com/in/{linkedin_username}',
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


        r = s.post('https://app.apollo.io/api/v1/contacts',
                   headers=extension_headers,
                   json=json_data)

        if r.status_code != 200:
            logging.warning("Contact apollo request failed, ", r.text)
            repeated_attempts += 1
            s = get_apollo_session()
            continue

        data = r.json()
        if data.get('contact') == {}:
            logging.warning('Not a person data, ', data)
            row = next(reader, None)
            continue

        email = data['contact']['email']
        row['Apollo Email'] = email

        logging.info(f'{linkedin_username}: {email}')
        
        # change account after every 100 requests
        if i == 100:
            i = 0
            s = get_apollo_session()

        final_data.append(row)
        repeated_attempts = 0
        row = next(reader, None)

    # TODO: write final_data to the final_path

    pd.DataFrame(final_data).to_csv('output.csv')
    csvfile.close()



if _name_ == '_main_':
    enrich()