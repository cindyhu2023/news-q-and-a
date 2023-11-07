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


questions = [
    "What happened during the shooting incident outside a southern Los Angeles grocery store that left six people injured?",
    "Why were three Pennsylvania officers charged with manslaughter in the fatal shooting of an 8-year-old?",
    "How is the reform-minded Los Angeles County DA, George Gascón, being threatened by package thefts and other high-profile crimes?",
    "What happened during the head-on crash that killed nine people and involved the University of the Southwest golf teams?",
    "How did Border Patrol rescue migrants in the Rio Grande?",
    "What is the significance of Punxsutawney Phil seeing his shadow and what does it mean for winter?",
    "Why was a bridge given an overall 'poor' rating by the Pennsylvania Department of Transportation?",
    "Why was an Oklahoma death row inmate who requested a firing squad executed by lethal injection?",
    "What is the Milwaukee Police's belief about the multiple suspects in the fatal shooting of six people?",
    "What happened to the 13-year-old boy who died after presumed fentanyl exposure at his Hartford, CT school, and what are the implications of this incident?",
]