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
    st.set_page_config(page_icon=":lightning", page_title="Genemail AI", layout="wide")

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    if "selected_chat" not in st.session_state:
        st.session_state.selected_chat = None
    st.sidebar.header(
        f"Genemail AI" if not st.session_state.selected_chat else f"Previous Sessions"
    )
    st.sidebar.text(f"Enter the job url and I'll write a cold email for you!")
    reset = st.sidebar.button("Reset") if st.session_state.chat_sessions else False
    if reset:
        st.session_state.clear()
        st.rerun()
    for chat in st.session_state.chat_sessions.keys():
        if st.sidebar.button(chat, key=f"selected-{chat}"):
            st.session_state.selected_chat = chat
    st.subheader((
        f"Welcome!"
        if not st.session_state.selected_chat
        else f"Job URL: {st.session_state.selected_chat}"
        ),
        anchor=False,
    )

    url_input = st.text_input(
        f"Enter the url to a job listing",
        value='' if not st.session_state.selected_chat else st.session_state.selected_chat,
    )
    if (
        st.session_state.selected_chat
        and st.session_state.selected_chat in st.session_state.chat_sessions.keys()
    ):
        st.write(st.session_state.chat_sessions[st.session_state.selected_chat])
    if url_input.strip() and not validators.url(url_input.strip()):
        st.error("Invalid URL! Please enter a valid job listing URL.")
        return
    if url_input.strip() != '':

        submit = st.button(
            'Submit', disabled=url_input.strip() == '' or not validators.url(url_input.strip())
        )

        if submit:
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
                        st.session_state.chat_sessions[url_input.strip()] = email_response
                        st.session_state.selected_chat = url_input.strip()
                        st.rerun()
            except Exception as e:
                st.info(e)


if __name__ == '__main__':
    app()