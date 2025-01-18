import os
import uuid
import pandas as pd
from chromadb_config import connect_chromadb

#Connect ChromaDB
client = connect_chromadb()

def load_collection(name, filename):
    filepath = os.path.join('assets', filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    pc = client.get_or_create_collection(name=name)
    df = pd.read_csv(filepath)

    if not pc.count():
        for row in df.iterrows():
            pc.add(
                documents=row[1]['Tech_Stack'],
                metadatas={'links': row[1]['Portfolio_Link']},
                ids=[str(uuid.uuid4())],
            )
    return pc



def get_query_results(collection, query_texts, n_results):
    return collection.query(query_texts=query_texts, n_results=n_results)

def get_links_from_collection(queries):
    pc = load_collection('portfolio_collection', 'techstack_portfolio.csv')
    pc.get()

    query_results = get_query_results(pc, queries, 2)
    return [val['links'] for val in query_results['metadatas'][0]]