from langchain_core.prompts import PromptTemplate
from model import llm_init

def chain_init(template, api_key):
    prompt = PromptTemplate.from_template(template=template)
    llm = llm_init(model="llama3-70b-8192", api_key=api_key, temperature=0.7)
    return prompt | llm

def extract_jobs(page_data, api_key):
    job_scraping_template = f'''
    ###SCRAPED TEXT FROM THE WEBSITE:
    {page_data}
    ###INSTRUCTIONS:
    The scraped text is from the website's homepage. Your job is to extract the job listings from the links and return them in JSON format containing the
    following keys: 'role', 'experience', 'skills', and 'description'.
    Only return the valid JSON.
    ###VALID JSON (NO PREAMBLE):
    '''
    chain = chain_init(job_scraping_template, api_key)
    return chain.invoke(input={'page_data': page_data})

def draft_email(job_desc, links, api_key):
    email_template = '''
    ###JOB DESCRIPTION:
    {job_desc}
    ###INSTRUCTIONS:
    You're Alex, a Business Development Associate at X. X is an AI & Software Consulting company dedicated to
    the seamless integration of business processes through automated tools.
    Over the years, we have empowered several enterprises with tailormade solutions:
    process optimization, cost reduction, and heightened overall efficiency.
    Your task is to write a cold email to the client regarding the jobs mentioned above
    fulfilling their needs.
    Also, add the most relevant ones from the following links to showcase X's portfolio {links}.
    Remember, you're Alex, BDA at X.
    Do not provide a preamble
    ###EMAIL (NO PREAMBLE):
    '''
    email_chain = chain_init(email_template, api_key)
    return email_chain.invoke(input={'job_desc': str(job_desc), 'links': links})