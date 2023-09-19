from langchain.llms import OpenAI
from langchain.chains import llm
from langchain.prompts import PromptTemplate
import os

open_ai_key = os.environ.get("OPENAI_API_KEY")
# llm = OpenAI(openai_api_key=open_ai_key)

llm_ai = OpenAI(temperature=0.9, openai_api_key=open_ai_key)
prompt_template = PromptTemplate(
    template="{about}:\n"
             "I want you to  "
             "based on the following criteria and urls:\n"
             "url: {url}\n"
)


def get_context_data():
    chained_llm = llm.LLMChain(llm=llm_ai, prompt=prompt_template)
    input_data = {

    }
    result = chained_llm.run(input_data)
    return result