from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import TextConverter, PreProcessor
import os
import re

def url_from_filename(filename):
    # Define a regular expression pattern to match the date and title part of the string
    pattern = r"(\d{4}-\d{2}-\d{2})-(.*?).txt"

    # Use re.search to find the matched groups in the input string
    match = re.search(pattern, filename)

    if match:
        # Extract the matched groups
        date_part = "/".join(match.group(1).split("-"))
        title_part = match.group(2)
        
        # Construct the URL
        url = f"https://localnewsinitiative.northwestern.edu/posts/{date_part}/{title_part}/index.html"

        return url
    else:
        return None

def initialize_document_store():
    document_store = ElasticsearchDocumentStore(host="localhost")
    text_converter = TextConverter()
    preprocessor = PreProcessor(
        clean_whitespace=True,
        clean_header_footer=True,
        clean_empty_lines=True,
        split_by="word",
        split_length=200,
        split_overlap=20,
        split_respect_sentence_boundary=True,
    )
    doc_dir = "posts_txt"
    document_count = 0
    chunk_count = 0
    print("=================WRITING DOCUMENTS=================")
    for filename in os.listdir(doc_dir):
        print("filename: ", filename)
        with open(os.path.join(doc_dir, filename), 'r', encoding='utf-8') as file:
            document_count += 1
            url = url_from_filename(filename)
            doc = text_converter.convert(file_path=doc_dir + "/" + filename, meta={"URL": url})
            chunks = preprocessor.process(doc)
            chunk_count += len(chunks)
            document_store.write_documents(chunks)
    print("=================DONE WRITING DOCUMENTS=================")
    print("document_count: ", document_count)
    print("chunk_count: ", chunk_count)
    return document_store

document_store = initialize_document_store()