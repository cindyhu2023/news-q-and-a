from flask import Flask, request, jsonify
from haystack.document_stores import OpenSearchDocumentStore
import logging
from haystack import Pipeline, Document
# from haystack.document import Document
from haystack.nodes import BM25Retriever, FARMReader, PromptModel, PromptNode, PromptTemplate, AnswerParser, EmbeddingRetriever
import os
from haystack.utils import print_answers
from dotenv import load_dotenv
import json

load_dotenv()

url = os.getenv("OPENSEARCH_URL")
username =  os.getenv("OPENSEARCH_USERNAME")
password = os.getenv("OPENSEARCH_PASSWORD")
document_store = OpenSearchDocumentStore(
    host=url, username=username, password=password, 
    port=443, verify_certs=True,
)

retriever = EmbeddingRetriever(
    document_store=document_store,
   embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
   model_format="sentence_transformers",
   top_k=3
)
# document_store.update_embeddings(retriever)

prompt_template1 = '''
        Create a concise and informative answer (around 50 words) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''

prompt_template2 = '''
        Create a concise answer (as short as possible) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''

prompt_template3 = '''
        Create a detailed and informative answer (up to 100 words) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''

prompt_template4 = '''
        Create a concise and informative answer (up to 50 words) for a given question based solely on the given documents.
        Use a journalistic and objective tone for the answer. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''

prompt_template5 = '''
        Create a concise and informative answer (up to 50 words) for a given question based solely on the given documents. 
        Use a casual and more approachable tone with a touch of humor for the answer.
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''

prompt_template6 = '''
        Create a concise and informative answer (up to 50 words) for a given question based solely on the given documents.
        Use a tone and wording that is appropriate for the general public and less-educated readers for the answer. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
'''


def query_openai(user_queries, retriever, model_name, prompt_template):
    openai_api_key = os.getenv("OPEN_AI_KEY")
    # question_answering_with_references = PromptTemplate("deepset/question-answering-with-references", output_parser=AnswerParser(reference_pattern=r"Document\[(\d+)\]"))
    question_answering_with_references = PromptTemplate(prompt=prompt_template, output_parser=AnswerParser(reference_pattern=r"Document\[(\d+)\]"))

    prompt_open_ai = PromptModel(model_name_or_path=model_name, api_key=openai_api_key)
    pn_open_ai = PromptNode(prompt_open_ai, default_prompt_template=question_answering_with_references)

    querying_pipeline = Pipeline()
    querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    # querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])
    querying_pipeline.add_node(component=pn_open_ai, name="prompt_node", inputs=["Retriever"])

    responses = []
    for i, query in enumerate(user_queries):
        output = querying_pipeline.run(query=query)
        # print("Output: ", output.keys())
        answer = output["answers"][0].answer
        reference = {}
        for idx, doc in enumerate(output["documents"]):
            reference[idx+1] = doc.meta["URL"]
        response = {
            "id": i,
            "question": query,
            "answer": answer,
            "reference": reference
        }
        responses.append(response)
        print("question ", i, ": ", query)
        print("answer ", i, ": ", answer)
        # print(output["documents"])

    return responses

questions = [
    "What's the damage of Colorado wildfire?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What pieces of evidence supported that Elizabeth Holmes is guilty?",
    "What are the economic challenges facing Britain, and how is the cost of living crisis impacting its citizens?",
    "How are major oil price fluctuations affecting gas prices, and what are the potential consequences for consumers?",
    "What is the US's stance on the Ukraine crisis?",
    "What is China's stance on the Ukraine crisis?",
    "Did the US send troops to Ukraine?",
    "Why are companies are moving out of Russia?",
    "Who is the first black woman in Supreme Court?",
    "Who is Ketanji Jackson?",
    "Who is Eileen Guo?",
    "What measures are the Chicago Teachers Union implementing to ensure the safety of in-person learning during the COVID-19 pandemic?"
]


tests = [
    # {
    #     "name": "response_length_standard.json",
    #     "retriever": EmbeddingRetriever(
    #         document_store=document_store,
    #         embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #         model_format="sentence_transformers",
    #         top_k=5
    #     ),
    #     "query_type": "openai",
    #     "model_name": "gpt-3.5-turbo",
    #     "prompt_template": prompt_template1
    # },
    # {
    #     "name": "response_length_short.json",
    #     "retriever": EmbeddingRetriever(
    #         document_store=document_store,
    #         embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #         model_format="sentence_transformers",
    #         top_k=5
    #     ),
    #     "query_type": "openai",
    #     "model_name": "gpt-3.5-turbo",
    #     "prompt_template": prompt_template2
    # },
    # {
    #     "name": "response_length_long.json",
    #     "retriever": EmbeddingRetriever(
    #         document_store=document_store,
    #         embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #         model_format="sentence_transformers",
    #         top_k=5
    #     ),
    #     "query_type": "openai",
    #     "model_name": "gpt-3.5-turbo",
    #     "prompt_template": prompt_template3
    # },
     {
        "name": "response_tone_standard.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=5
        ),
        "query_type": "openai",
        "model_name": "gpt-3.5-turbo",
        "prompt_template": prompt_template4
    },
    {
        "name": "response_tone_casual.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=5
        ),
        "query_type": "openai",
        "model_name": "gpt-3.5-turbo",
        "prompt_template": prompt_template5
    },
    {
        "name": "response_tone_general_public.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=5
        ),
        "query_type": "openai",
        "model_name": "gpt-3.5-turbo",
        "prompt_template": prompt_template6
    },

]
def run():
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.INFO)
    logging.getLogger("haystack").setLevel(logging.INFO)
    for test in tests:
        print("Running test: ", test["name"])
        if test["query_type"] == "openai":
            responses = query_openai(questions, test["retriever"], test["model_name"], test["prompt_template"])
        else:
            responses = []
        with open(test["name"], 'w') as outfile:
            json.dump(responses, outfile)
    return

run()

