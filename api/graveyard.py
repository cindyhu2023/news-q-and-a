# Initialize the document store and indexing pipeline
def initialize_document_store_and_pipeline():
    document_store = ElasticsearchDocumentStore(host="localhost")
    indexing_pipeline = Pipeline()
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
    indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
    indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])
    doc_dir = "posts_txt"
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    indexing_pipeline.run(file_paths=files_to_index)

    return document_store, indexing_pipeline

document_store, indexing_pipeline = initialize_document_store_and_pipeline()