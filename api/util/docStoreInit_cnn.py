from haystack.document_stores import ElasticsearchDocumentStore, OpenSearchDocumentStore
from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack.schema import Document
import os
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

# chunking news articles and inserting into OpenSearch
def initialize_document_store(document_store):
    # initialize preprocessor to 200 words per chunk
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
    chunks = []
    print("=================WRITING DOCUMENTS=================")
    df = pd.read_csv(doc_dir)
    for index, row in df.iterrows():
        document_count += 1
        doc = Document(content=row['Article text'], meta={"URL": row['Url'], "Date published": row['Date published'], "Headline": row['Headline']})
        chunks += preprocessor.process([doc])

        # write to OpenSearch in chunks of 50 news articles
        if document_count % 50 == 0:
            document_store.write_documents(chunks)
            chunks = []
    if len(chunks) > 0:
        document_store.write_documents(chunks)
    print("=================DONE WRITING DOCUMENTS=================")
    print("total document_count: ", document_count)
    return document_store

# update embeddings to allow for semantic search
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


# initialize document store for ElasticSearch or OpenSearch
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
        document_store = update_embeddings(document_store)
        return document_store
    else:
        return None

document_store = run("opensearch")