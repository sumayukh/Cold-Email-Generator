import os
import streamlit as st
import validators
from chain import draft_email, extract_jobs
from dotenv import load_dotenv
from langchain.output_parsers.json import SimpleJsonOutputParser
from portfolio import get_links_from_collection
from web_scraper import job_listing_scraper

load_dotenv()

url = os.getenv('JOB_URL')
json_parser = SimpleJsonOutputParser()

def app():
    st.title('Cold Email Generator', anchor=False)
    url_input = st.text_input("Enter the url to a job listing")

    st.sidebar.header(f"Enter the job url and I'll write a cold email for you!")
    
    submit = st.sidebar.button(
        'Submit', disabled=url_input.strip() == '' or not validators.url(url_input.strip())
    )

    if url_input.strip() and not validators.url(url_input.strip()):
        st.error("Invalid URL! Please enter a valid job listing URL.")
        return
    if submit and url_input.strip() != '':
        page_data = job_listing_scraper(url_input.strip())
        try:
            output = extract_jobs(page_data, os.getenv("GROQ_API_KEY"))
            if not output:
                st.error('Could not generate output')
            else:
                response = json_parser.parse(output.content)[0]
                skill_set = response['skills']
                links = get_links_from_collection(skill_set)
                email_output = draft_email(response, links, os.getenv("GROQ_API_KEY"))
                if not email_output:
                    st.error('Could not generate email')
                else:
                    email_response = email_output.content
                    st.write(email_response)
        except Exception as e:
            print(f"Error: {e}, Error type: {type(e)}")
            st.error('Something went wrong! Please check logs for more.')


if __name__ == '__main__':
    app()