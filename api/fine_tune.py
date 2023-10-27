from flask import Flask, request, jsonify
from haystack.document_stores import ElasticsearchDocumentStore
import logging
from haystack import Pipeline, Document
# from haystack.document import Document
from haystack.nodes import TextConverter, PreProcessor, BM25Retriever, FARMReader, PromptModel, PromptNode, PromptTemplate, AnswerParser
import os
from haystack.utils import print_answers
from dotenv import load_dotenv

load_dotenv()

document_store = ElasticsearchDocumentStore(host="localhost")

# Set up the retriever and reader
def setup_retriever_and_reader():
    retriever = BM25Retriever(document_store=document_store, top_k=5)
    # reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
    reader = FARMReader(model_name_or_path="deepset/bert-large-uncased-whole-word-masking-squad2", use_gpu=False)
    return retriever, reader

retriever, reader = setup_retriever_and_reader()


def query(user_query, retriever, reader):
    openai_api_key = os.getenv("OPEN_AI_KEY")
    prompt_template = '''
        Create a concise and informative answer (no more than 50 words) for a given question 
        based solely on the given documents. You must only use information from the given documents. 
        Use an unbiased and journalistic tone. Do not repeat text.
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1] next to the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''
    # question_answering_with_references = PromptTemplate("deepset/question-answering-with-references", output_parser=AnswerParser(reference_pattern=r"Document\[(\d+)\]"))
    question_answering_with_references = PromptTemplate(prompt=prompt_template, output_parser=AnswerParser(reference_pattern=r"Document\[(\d+)\]"))

    prompt_open_ai = PromptModel(model_name_or_path="text-davinci-003", api_key=openai_api_key)
    pn_open_ai = PromptNode(prompt_open_ai, default_prompt_template=question_answering_with_references)

    querying_pipeline = Pipeline()
    querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])
    querying_pipeline.add_node(component=pn_open_ai, name="prompt_node", inputs=["Retriever"])
    output = querying_pipeline.run(query=user_query)
    # print("Output: ", output.keys())
    answer = output["answers"][0].answer
    reference = {}
    for idx, doc in enumerate(output["documents"]):
        reference[idx+1] = doc.meta["URL"]

    return answer, reference

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

top_k = [3, 5, 7]
reader_model = [""]

def run():
    for question in questions:
        answer, reference = query(question, retriever, reader)
        print("Question: ")
        print(question)
        print("Answer: ")
        print(answer)
        print("Reference: ")
        print(reference)
        print("=====================================")

    return

run()


