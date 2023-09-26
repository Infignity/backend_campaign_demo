from langchain.prompts import PromptTemplate


# campaign_template = PromptTemplate(
#     input_variables=['company_data', 'company_json'],
#     template="You are an Organization Job and Company Campaign Analyst \n"
#     "using the company analyzed result {company}: \n"
#     "Filter the data using company job_title, job_title_role, and experience, and provide the filtered data in the following format under the subject 'Filtered Data':\n\n"
#     "Filtered Data:\n"
#     "1. Job Title: [List of job titles]\n"
#     "2. Job Title Role: [List of job title roles]\n"
#     "3. Experience: [List of experiences]\n"
# )

campaign_temps = PromptTemplate(
    input_variables=['company_data', 'company_json'],
    template="You are an Organization Job and Company Campaign Analyst responsible for analyzing company data and identifying jobs based on company scraped data and LinkedIn information.\n"
    "Your task is to analyze the potential job advertisements and campaigns from the company's scraped data:\n\n"
    "Company Scraped Data:\n"
    "{company_data}\n\n"
    "LinkedIn Data:\n"
    "{company_json}\n\n"
    "Filter the data using company job_title, job_title_role, and experience, and provide the filtered data in the following format under the subject 'Filtered Data':\n\n"
    "Filtered Data:\n"
    "1. Job Title: [List of job titles]\n"
    "2. Job Title Role: [List of job title roles]\n"
    "3. Experience: [List of experiences]\n"
    "4. Reason: [in paragraph, why the chosen filters makes sense in a descriptive manner, don't use word Linkedin, tell why the data points from these filters may buy the company. Include company name and product if available.]\n"
)
campaign_template = PromptTemplate(
    input_variables=['company_data', 'company_json'],
    template= "You are an Organization Job and Company Campaign Analyst responsible for analyzing company data and identifying jobs based on a company scraped data {company_data} and LinkedIn information {company_json}.\n"
    "Your task is to analyze the potential job advertisements and campaigns from the company's scraped data. You have to find best prospects to reach to sell the company product. \n" 
    "Give linkedin filters for potentials clients of the company and the reason why those filters are the best. \n" 
    "Strictly in the below format and order:\n"
    "Filtered Data:\n"
    "1. Job Title [list of job title, not more than 3, comma separated]\n"
    "2. Countries [list of countries, not more than 2, comma separated]\n"
    "3. Keywords [not more than 4, comma separated]\n"
    "4. Reason: paragraph why the filters makes sense in a descriptive manner, don't use word Linkedin, tell why the data points from these filters may buy the company. Include company name and product if available.\n"
)
analyst_template = PromptTemplate(
    input_variables=['company_data', 'company_json'],
    template="You are an Organization System Analyst responsible for analyzing company data. Your goal is to provide a comprehensive analysis of the company's operations based on the provided data. Please use facts about the company as much as possible.\n"
    "Analyze the company's record considering the following data filters and output format:\n\n"
    "1. Problems Addressed:\n"
    "   1.a. Problems Identified:\n"
    "       - [List of identified problems]\n"
    "   1.b. Solutions Offered:\n"
    "       - [List of offered solutions]\n\n"
    "2. Buyer Persona:\n"
    "   2.a. Demographics:\n"
    "       - [Demographic details]\n"
    "   2.b. Behavioral Traits:\n"
    "       - [Behavioral traits]\n"
    "   2.c. Motivations & Goals:\n"
    "       - [Motivations and goals]\n\n"
    "3. Target Market:\n"
    "   3.a. Segmentation:\n"
    "       - [Market segmentation details]\n"
    "   3.b. Potential Reach:\n"
    "       - [Potential reach information]\n"
    "   3.c. Market Size & Growth:\n"
    "       - [Market size and growth details]\n\n"
    "4. Company Summary:\n"
    "   - [Company summary]\n\n"
    "In your analysis, consider the company's LinkedIn data presented in JSON format:\n"
    "{company_json}\n\n"
    "and the company website scrapped data:\n"
    "{company_data}\n\n"
)

# "Additionally, filter the data using company job_title, job_title_role, and experience, and provide the filtered data in the following format under the subject 'Filtered Data':\n\n"
# "Filtered Data:\n"
# "1. Job Title: [List of job titles]\n"
# "2. Job Title Role: [List of job title roles]\n"
# "3. Experience: [List of experiences]\n"

campaign_template_sec = PromptTemplate(
    input_variables=['company_data', 'company_json'],
    template="You are an Organization Job Analyst responsible for analyzing company data and identifying jobs from a company scrapped data and linkedin information\n"
    "anaylse the company potential job advert and campaign from company scrapped data:{company_data} and their linkedin data {company_json} \n"
    "filter the data using company job_title, job_title_role, and experience. Provide the filtered data in the format of numbered lists under the subject \n"
    "Filtered Data: \n"
)

analyst_template_sec = PromptTemplate(
    input_variables=['company_data', 'company_json'],
    template="You are an Organization System Analyst responsible for analyzing company data. Your goal is to provide a comprehensive analysis of the company's operations based on the provided data. Please use facts about the company as much as possible"
    "anaylse the company record considering the data filters as follows:\n"
    "problem addressed which described the problem identified, solution offerred \n"
    "Buyer Persona: considering the demographic, behavioural trait, motivation and goals\n"
    "Target Market: considering the segmentation, potential reach, market size and growth\n"
    "Company Summary: \n"
    "in your analysis consider the company's LinkedIn data presented in JSON format {company_json} \n"
    "and also the company scrapped data : {company_data}"
    "Additionally, filter the data using company job_title, job_title_role, and experience. Provide the filtered data in the format of numbered lists under the subject \n"
    "Filtered Data: \n"
)

email_prompt = PromptTemplate(
    input_variables=['company_data', 'person_json_data'],
    template="You are an email writer. Which writes hyper personal email, and uses the relevent personal points to get the point across.\n"
    "You are give a company data and person's data in json format.\n" 
    "Use that to generate an email selling the company's product to the person.\n"
    "Choose a sender's name and his position in the company. \n"
    "Focus on why the person would benefit from the company's product and use his education, previous experience, country, skills, etc. to give a personal touch. Restrict to 3 paragraphs only. Keep the tone professional.\n"
    "company data: {company_data} \n\n"
    "person's json data: {person_json_data}"
)
