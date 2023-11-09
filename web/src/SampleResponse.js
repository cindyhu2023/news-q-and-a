// a react component that displays questions and responses from responses.json
import React, { useEffect } from 'react';
// import data from './test_response/responses.json';
import test1 from './test_response_2/plain_3_openai.json';
import test2 from './test_response_2/embedding_5_openai.json';
import test3 from './test_response_2/embedding_3_openai.json'; 

const tests = [
    {
        "name": "plain_3_openai",
        "response": test1
    },
    {
        "name": "embedding_3_openai",
        "response": test3
    },
    {
        "name": "embedding_5_openai",
        "response": test2
    },
]

const questions = [
    "What's the damage of Colorado wildfire?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What's the number of COVID-19 cases in the US?",
    "What is the new COVID-19 variant?",
    "What are the economic challenges facing Britain, and how is the cost of living crisis impacting its citizens?",
    "How are major oil price fluctuations affecting gas prices, and what are the potential consequences for consumers?What is the US's stance on the Ukraine crisis?",
    "What is China's stance on the Ukraine crisis?",
    "Did the US send troops to Ukraine?",
    "What companies are moving out of Russia and why?",
    "Who is the first black woman in Supreme Court?",
    "Who is Ketanji Jackson?",
    "Who is Eileen Guo?",
    "What measures are the Chicago Teachers Union implementing to ensure the safety of in-person learning during the COVID-19 pandemic?"
]

function SampleResponse(){
    // display one question and its response, click "next" to display the next question and response
    const [index, setIndex] = React.useState(0);
    function submit(){
        console.log("submit");
    }
    return (
        <div>
        <p><em>{questions[index]}</em></p>
        <p>{tests[0].response[index].answer}</p>
        <p>{tests[1].response[index].answer}</p>
        <p>{tests[2].response[index].answer}</p>
        <button onClick={() => setIndex((index + 1) % questions.length)}>back</button>
        {
            index === questions.length - 1 ? <button onClick={submit}>submit</button> : <button onClick={() => setIndex((index + 1) % questions.length)}>next</button>
        }
        </div>
    )

}

export default SampleResponse;