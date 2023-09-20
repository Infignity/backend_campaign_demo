'''importing program modules'''
import os
from urllib.parse import urlparse
from langchain.llms import OpenAI
from langchain.chains import llm
from langchain.prompts import PromptTemplate


# TODO: using cloudflare tunnel to host
open_ai_key = os.environ.get("OPENAI_API_KEY")
# llm = OpenAI(openai_api_key=open_ai_key)
llm_ai = OpenAI(temperature=0.9, openai_api_key=open_ai_key)
prompt_templatex = PromptTemplate(
    input_variables=['url'],
    template="about us getter:\n"
             "I want you to  provide an about for the company from"
             "based on the following criteria and urls:\n"
             "url: {url}\n"
)


def get_ai_data(url, prompt_template):
    ''' a llm function to get data base on some content'''
    chained_llm = llm.LLMChain(llm=llm_ai, prompt=prompt_template)
    input_data = {
        # 'about': about,
        'url': url,
       }
    result = chained_llm.run(input_data)
    return result


def domain_related_route(urls, target_domain):
    '''get webpages on same domain'''
    # Initialize a list to store URLs with the same domain
    same_domain_urls = []
    # Check if the target_domain ends with a forward slash
    if target_domain.endswith('/'):
        # Remove the trailing forward slash
        target_domain = target_domain[:-1]
    for url in urls:
        # Check if the URL starts with "#" (internal link) or is empty
        if url.startswith("#") or not url.strip():
            continue
        # Parse the URL to extract the domain
        parsed_url = urlparse(url)
        url_domain = parsed_url.scheme + "://" + parsed_url.netloc

        # Check if the domain matches the target domain
        if url_domain == target_domain:
            same_domain_urls.append(url)
            print(url)
    return same_domain_urls[:10]
