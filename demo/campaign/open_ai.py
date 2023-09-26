'''importing program modules'''
import os
import re
from langchain.llms import OpenAI
from langchain.chains import llm
from .templates import analyst_template, campaign_template, email_prompt
# analyst_template, campaign_template, email_prompt


class LangChainAI:
    '''Company Data analysis'''
    def __init__(self):
        self.open_ai_key = os.environ.get("OPENAI_API_KEY")
        self.llm_ai = OpenAI(temperature=0.9, openai_api_key=self.open_ai_key)

    def analysis_extractor(self, text):
        '''extract the company analyzed data'''
        print(text)
        # regular expression pattern to match section headers and their content
        pattern = r'([0-9]+\.[a-z]+\.[a-zA-Z\s]+:\n(?:-\s[^\n]+\n)+)'
        # Using re.findall to find all matching sections
        sections = re.findall(pattern, text)
        data = {}
        # Iterate through the matched sections and extract data
        for section in sections:
            lines = section.strip().split('\n')
            header = lines[0].strip()
            content = [line.strip('- ').strip() for line in lines[1:]]
            data[header] = content
        return data
    
    def job_analysis_extractor(self, text):
        '''job list extractors'''
        # a regular exp pattern to match numbered list items along with headers
        pattern = r'(?P<number>\d+)\.\s(?P<header>[^:]+):\s(?P<items>.+)'

        # Use re.finditer to find all matching sections
        matches = re.finditer(pattern, text)
        data = {}
        # Iterate through the matched sections and extract data
        for match in matches:
            header = match.group('header').strip()  # Extract the header
            items = match.group('items').strip().split(', ')
            data[header] = items
        return data

    def extract_and_format_data(self, text):
        """extract dataset"""
        # Initialize a dictionary to store extracted data
        extracted_data = {}
        # Split the text into lines
        lines = text.split('\n')

        # Initialize variables to track the current section and data
        current_section = None
        current_data = []
        # Iterate through each line and extract data
        for line in lines:
            # Check if the line matches a header pattern
            header_match = re.match(r'^([A-Z][a-zA-Z\s&]+):$', line.strip())
            if header_match:
                # If a new header is found, store the previous data (if any)
                if current_section and current_data:
                    extracted_data[current_section] = '\n'.join(current_data)
                    current_data = []

                # Extract the header text (without the colon)
                current_section = header_match.group(1)
            else:
                # Store the line as data under the current section
                if current_section:
                    current_data.append(line.strip())

        # Store the last section's data (if any)
        if current_section and current_data:
            extracted_data[current_section] = '\n'.join(current_data)
        return extracted_data
    
    def reduce_prompt_length(self, text, max_tokens=2000):
        """
        Truncate the input text to the specified maximum number of tokens.
        """
        tokens = text.split()
        if len(tokens) <= max_tokens:
            return text
        else:
            return ' '.join(tokens[:max_tokens])

    def get_ai_data(self, company_data, json_data):
        ''' a llm function to get data base on some content'''
        chained_llm = llm.LLMChain(
            llm=self.llm_ai,
            prompt=analyst_template
        )
        print(company_data)
        company_text = ' '.join(company_data)
        truncated_data = self.reduce_prompt_length(company_text, 500)
        input_data = {
            'company_data': truncated_data,
            'company_json': json_data,
        }
        analysis_result = chained_llm.run(input_data)
        # print(data)
        # analysis_result = self.extract_and_format_data(data)
        print(analysis_result)
        print("="*10, 'analysis data', "="*10,)
        # analyze the job description
        
        campaign_llm = llm.LLMChain(
            llm=self.llm_ai,
            prompt=campaign_template
        )
        campaign_data = campaign_llm.run(input_data)
        campaign_result = self.job_analysis_extractor(campaign_data)
        print(campaign_result)
        print("="*10, 'campaign data', "="*10,)
        
        return analysis_result, campaign_result

    def email_generator(
            self,
            person_json_data,
            company_data):
        ''' an email generator language model'''
        
        chained_llm = llm.LLMChain(
            llm=self.llm_ai,
            prompt=email_prompt
        )
        input_data = {
            'company_data': company_data,
            'person_json_data': person_json_data
        }
        data = chained_llm.run(input_data)
        return data
