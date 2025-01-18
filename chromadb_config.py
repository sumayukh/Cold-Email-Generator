import chromadb

#Connect Chroma(Vector DB)
def connect_chromadb():
    return chromadb.PersistentClient('vector_db')