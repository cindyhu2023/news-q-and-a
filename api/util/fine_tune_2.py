from flask import Flask, request, jsonify
from haystack.document_stores import ElasticsearchDocumentStore
import logging
from haystack import Pipeline, Document
# from haystack.document import Document
from haystack.nodes import TextConverter, PreProcessor, BM25Retriever, FARMReader, PromptModel, PromptNode, PromptTemplate, AnswerParser, EmbeddingRetriever
import os
from haystack.utils import print_answers
from dotenv import load_dotenv
import json

load_dotenv()

# document_store = ElasticsearchDocumentStore(host="localhost")

# # Set up the retriever and reader
# def setup_retriever_and_reader():
#     retriever = BM25Retriever(document_store=document_store, top_k=10)
#     # reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)
#     # reader = FARMReader(model_name_or_path="deepset/bert-large-uncased-whole-word-masking-squad2", use_gpu=False)
#     return retriever

# retriever = setup_retriever_and_reader()

document_store = ElasticsearchDocumentStore(
    similarity="dot_product",
    embedding_dim=768
)
retriever = EmbeddingRetriever(
    document_store=document_store,
   embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
   model_format="sentence_transformers",
   top_k=5
)
# document_store.update_embeddings(retriever)


def query_openai(user_queries, retriever, model_name):
    openai_api_key = os.getenv("OPEN_AI_KEY")
    prompt_template = '''
        Create a concise and informative answer (no more than 50 words) for a given question based solely on the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] next to the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''
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

def query_reader(questions, retriever, model_name):
    reader = FARMReader(model_name_or_path=model_name, use_gpu=False)
    # reader = FARMReader(model_name_or_path=model_name, use_gpu=False)
    querying_pipeline = Pipeline()
    querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])

    responses = []
    for i, query in enumerate(questions):
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

    return responses

questions = [
    "What's the damage of Colorado wildfire?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What's the number of COVID-19 cases in the US?",
    "What is the new COVID-19 variant?",
    "What are the economic challenges facing Britain, and how is the cost of living crisis impacting its citizens?",
    "How are major oil price fluctuations affecting gas prices, and what are the potential consequences for consumers?",
    "What is the US's stance on the Ukraine crisis?",
    "What is China's stance on the Ukraine crisis?",
    "Did the US send troops to Ukraine?",
    "What companies are moving out of Russia and why?",
    "Who is the first black woman in Supreme Court?",
    "Who is Ketanji Jackson?",
    "Who is Eileen Guo?",
    "What measures are the Chicago Teachers Union implementing to ensure the safety of in-person learning during the COVID-19 pandemic?"
]


tests = [
    {
        "name": "plain_3_openai.json",
        "retriever": BM25Retriever(document_store=document_store, top_k=3),
        "query_type": "openai",
        "model_name": "text-davinci-003"
    },
    {
        "name": "embedding_3_openai.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=3
        ),
        "query_type": "openai",
        "model_name": "text-davinci-003"
    },
    {
        "name": "embedding_5_openai.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=5
        ),
        "query_type": "openai",
        "model_name": "text-davinci-003"
    },
    {
        "name": "plain_10_roberta.json",
        "retriever": BM25Retriever(document_store=document_store, top_k=10),
        "query_type": "reader",
        "model_name": "deepset/roberta-base-squad2"
    },
    {
        "name": "embedding_10_roberta.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=10
        ),
        "query_type": "reader",
        "model_name": "deepset/roberta-base-squad2"
    },
    {
        "name": "embedding_10_distilbert.json",
        "retriever": EmbeddingRetriever(
            document_store=document_store,
            embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
            model_format="sentence_transformers",
            top_k=10
        ),
        "query_type": "reader",
        "model_name": "distilbert-base-uncased-distilled-squad"
    }
]
def run():
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.INFO)
    logging.getLogger("haystack").setLevel(logging.INFO)
    for test in tests:
        print("Running test: ", test["name"])
        if test["query_type"] == "openai":
            responses = query_openai(questions, test["retriever"], test["model_name"])
        elif test["query_type"] == "reader":
            responses = query_reader(questions, test["retriever"], test["model_name"])
        else:
            responses = []
        with open(test["name"], 'w') as outfile:
            json.dump(responses, outfile)
    return

run()


'''
    Answer in less than 50 words with 2022 CNN news: What's the damage of Colorado wildfire? 
    Answer in less than 50 words with 2022 CNN news: Why is Elizabeth Holmes on trial?
    Answer in less than 50 words with 2022 CNN news: Is Elizabeth Holmes guilty?
    Answer in less than 50 words with 2022 CNN news: What's the number of COVID-19 cases in the US?
    Answer in less than 50 words with 2022 CNN news: What is the new COVID-19 variant?
    Answer in less than 50 words with 2022 CNN news: What are the economic challenges facing Britain, and how is the cost of living crisis impacting its citizens?
    Answer in less than 50 words with 2022 CNN news: How are major oil price fluctuations affecting gas prices, and what are the potential consequences for consumers
    Answer in less than 50 words with 2022 CNN news: What is the US's stance on the Ukraine crisis?
    Answer in less than 50 words with 2022 CNN news: What is China's stance on the Ukraine crisis?
    Answer in less than 50 words with 2022 CNN news: Did the US send troops to Ukraine?
    Answer in less than 50 words with 2022 CNN news: What companies are moving out of Russia and why?
    Answer in less than 50 words with 2022 CNN news: Who is the first black woman in Supreme Court?
    Answer in less than 50 words with 2022 CNN news: Who is Ketanji Jackson?
    Answer in less than 50 words with 2022 CNN news: Who is Eileen Guo?
    Answer in less than 50 words with 2022 CNN news: What measures are the Chicago Teachers Union implementing to ensure the safety of in-person learning during the COVID-19 pandemic?


'''