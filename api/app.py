from flask import Flask, request, jsonify
from haystack.document_stores import ElasticsearchDocumentStore, OpenSearchDocumentStore
import logging
from haystack import Pipeline
from haystack.nodes import PromptModel, PromptNode, PromptTemplate, AnswerParser, EmbeddingRetriever
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import datetime
import pytz
import json

load_dotenv()

# Initializing flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

def setup_logging(logging_level):
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging_level)
    logging.getLogger("haystack").setLevel(logging_level)

# document_store = ElasticsearchDocumentStore(host="localhost")

################## MYSQL LOGGING ##################
app.config['MYSQL_HOST'] = os.getenv("RDS_ENDPOINT")
app.config['MYSQL_USER'] = os.getenv("USER_NAME")
app.config['MYSQL_PASSWORD'] = os.getenv("USER_PWD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")

mysql = MySQL(app)

################## OPEN SEARCH ##################
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
    top_k=5
)

def query(user_query, retriever):
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
    # querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])
    querying_pipeline.add_node(component=pn_open_ai, name="prompt_node", inputs=["Retriever"])
    output = querying_pipeline.run(query=user_query)
    print("Output: ", output.keys())
    answer = output["answers"][0].answer
    reference = {}
    for idx, doc in enumerate(output["documents"]):
        reference[idx+1] = doc.meta["URL"]

    return answer, reference

@app.route('/question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    answer, reference = query(question, retriever)
    print("Answer: ", answer)
    print("Reference: ", reference)
    
    if question:
        response_data = {
            'question': question,
            'answer': answer,
            'reference': reference,
            'endpoint': os.getenv("RDS_ENDPOINT")
        }

        # log to database
        current_time_ct = datetime.datetime.now(pytz.timezone('US/Central'))
        current_time_string = current_time_ct.strftime('%Y-%m-%d %H:%M:%S %Z')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO qaRecord (question, answer, reference, timestamp) VALUES(%s, %s, %s, %s)", (question, answer, json.dumps(reference), current_time_string))
        mysql.connection.commit()
        cur.close()

        return jsonify(response_data) 
    else:
        return jsonify({'error': 'Question not provided.'}), 400  # Return error as JSON

    
# Running app
# if __name__ == '__main__':
#     setup_logging(logging.INFO)
#     app.run()
