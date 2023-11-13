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
from openai import OpenAI

load_dotenv()

# Initializing flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.INFO)
logging.getLogger("haystack").setLevel(logging.INFO)

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
    client = OpenAI(
        api_key=os.getenv("OPEN_AI_KEY")
    )
    prompt_template = '''
        Create a concise and informative answer (no more than 50 words) for a given question 
        based solely on the given documents. You must only use information from the given documents. 
        Cite the documents using numeric references in the text. 
        If multiple documents contain the answer, cite those documents like [1,2] at the end of the sentence in the answer. 
        If the documents do not contain the answer to the question, say that 'answering is not possible given the available information.'

        {join(documents, delimiter=new_line, pattern=new_line+'Document[$idx]: $content', str_replace={new_line: ' ', '[': '(', ']': ')'})}

        Question: {query}; Answer:
    '''

    documents = retriever.retrieve(query=user_query)
    prompt_template_obj = PromptTemplate(prompt=prompt_template)
    filled_prompt = list(prompt_template_obj.fill(documents=documents, query=user_query))[0]
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": filled_prompt,
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=1024,
    )

    answer = chat_completion.choices[0].message.content
    reference = {}
    for idx, doc in enumerate(documents):
        reference[idx+1] = doc.meta["URL"]
    answer, reference = remove_duplicate_references(answer, reference)

    return answer, reference

@app.route('/question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    answer, reference = query(question, retriever)
    
    if question:
        response_data = {
            'question': question,
            'answer': answer,
            'reference': reference,
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

@app.route('/log', methods=['POST'])
def log_response():
    body = request.get_json()
    print(body)
    session = body.get('sessionId')
    responses = body.get('data')
    current_time_ct = datetime.datetime.now(pytz.timezone('US/Central'))
    current_time_string = current_time_ct.strftime('%Y-%m-%d %H:%M:%S %Z')
    if session and responses:
        for i in ['0','1','2']:
            response = responses[i]
            question = response.get('question')
            answer = response.get('answer')
            comment = response.get('reason')

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO sampleResponses (timestamp, sessionId, question, answer, comment) VALUES(%s, %s, %s, %s, %s)", (current_time_string, session, question, answer, comment))
            mysql.connection.commit()
            cur.close()

        return jsonify({'msg': 'Logged response.'}), 200 
    else:
        return jsonify({'msg': 'Error!'}), 400  # Return error as JSON
    
# Running app
# if __name__ == '__main__':
#     setup_logging(logging.INFO)
#     app.run()

####### util functions #######

def remove_duplicate_references(answer, references):
    answer = answer.replace("[", "|")
    answer = answer.replace("]", "|")
    answer_list = answer.split("|")
    unique_references = {}
    url_to_index = {}
    next_index = 1
    res = ""
    for i, item in enumerate(answer_list):
        if i % 2 == 0:
            res += item
            continue
        else:
            refs = item.replace(" ", "").split(",")
            curr = []
            for ref in refs:
                if ref in curr:
                    continue
                elif references[int(ref)] not in url_to_index:
                    url_to_index[references[int(ref)]] = str(next_index)
                    unique_references[next_index] = references[int(ref)]
                    curr.append(str(next_index))
                    next_index += 1
                else:
                    new_ref = url_to_index[references[int(ref)]]
                    if new_ref not in curr:
                        curr.append(new_ref)
            new_item = ",".join(curr)
            res += "[" + new_item + "]" if new_item else ""


    return res, unique_references
