from langchain_community.document_loaders import WebBaseLoader
def job_listing_scraper(url):
    web_loader = WebBaseLoader(web_path=url)
    return web_loader.load().pop().page_content