from haystack.document_stores import ElasticsearchDocumentStore, OpenSearchDocumentStore
from haystack.nodes import TextConverter, PreProcessor, EmbeddingRetriever
from haystack.schema import Document
import os
import re
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

def initialize_document_store(document_store):
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=200,
        split_respect_sentence_boundary=True,
        progress_bar=False
    )
    doc_dir = "cnn/CNN_Articles_2022.csv"
    document_count = 0
    total_chunks = 0
    chunks = []
    print("=================WRITING DOCUMENTS=================")
    df = pd.read_csv(doc_dir)
    for index, row in df.iterrows():
        document_count += 1
        doc = Document(content=row['Article text'], meta={"URL": row['Url'], "Date published": row['Date published'], "Headline": row['Headline']})
        chunks += preprocessor.process([doc])
        # print("chunk_count: ", len(chunks))
        if document_count % 50 == 0:
            document_store.write_documents(chunks)
            total_chunks += len(chunks)
            chunks = []
            print("document_count: ", document_count)
    if len(chunks) > 0:
        document_store.write_documents(chunks)
        total_chunks += len(chunks)
    print("=================DONE WRITING DOCUMENTS=================")
    print("total document_count: ", document_count)
    print("total chunk_count: ", total_chunks)
    return document_store

def update_embeddings(document_store):
    print("=================UPDATING EMBEDDINGS=================")
    retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_format="sentence_transformers",
    top_k=5
    )
    document_store.update_embeddings(retriever)
    print("=================DONE UPDATING EMBEDDINGS=================")
    return document_store


def run(search_type):
    if search_type == "elastic":
        document_store = ElasticsearchDocumentStore(
        similarity="dot_product",
        embedding_dim=768
    )
        document_store = initialize_document_store(document_store)
        document_store = update_embeddings(document_store)
        return document_store
    elif search_type == "opensearch":
        url = os.getenv("OPENSEARCH_URL")
        username =  os.getenv("OPENSEARCH_USERNAME")
        password = os.getenv("OPENSEARCH_PASSWORD")
        document_store = OpenSearchDocumentStore(
            host=url, username=username, password=password, 
            port=443, verify_certs=True,
            similarity="dot_product",
            embedding_dim=768
        )
        document_store = initialize_document_store(document_store)
        input("Done initializing, press Enter to continue...")
        document_store = update_embeddings(document_store)
        return document_store
    else:
        return None

document_store = run("opensearch")