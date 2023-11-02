from haystack.document_stores import ElasticsearchDocumentStore, OpenSearchDocumentStore
from haystack.nodes import TextConverter, PreProcessor
from haystack.schema import Document
import os
import re
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

def initialize_document_store():
    document_store = ElasticsearchDocumentStore(host="localhost")
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="sentence",
        split_length=10,
        split_respect_sentence_boundary=False
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

def initialize_opensearch_store():
    url = os.getenv("OPENSEARCH_URL")
    username =  os.getenv("OPENSEARCH_USERNAME")
    password = os.getenv("OPENSEARCH_PASSWORD")
    document_store = OpenSearchDocumentStore(host=url, username=username, password=password, port=443, verify_certs=True)
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="sentence",
        split_length=10,
        split_respect_sentence_boundary=False
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


document_store = initialize_document_store()