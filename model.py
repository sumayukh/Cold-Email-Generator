from langchain_groq import ChatGroq

# Step 1: LLM setup using langchain
def llm_init(model, api_key, temperature):
    return ChatGroq(model=model, api_key=api_key, temperature=temperature, max_retries=2)