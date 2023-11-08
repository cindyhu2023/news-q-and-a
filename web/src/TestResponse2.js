// a react component that displays questions and responses from responses.json
import React, { useEffect } from 'react';
// import data from './test_response/responses.json';
import test1 from './test_response_2/plain_3_openai.json';
import test2 from './test_response_2/embedding_5_openai.json';
import test3 from './test_response_2/embedding_3_openai.json'; 
import test4 from './test_response_2/plain_10_roberta.json';
import test5 from './test_response_2/embedding_10_roberta.json';
import test6 from './test_response_2/embedding_10_distilbert.json';

import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

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
    {
        "name": "plain_10_reader_roberta",
        "response": test4
    },
    {
        "name": "embedding_10_reader_roberta",
        "response": test5
    },
    {
        "name": "embedding_10_reader_distilled",
        "response": test6
    }

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


function TestResponse2() {
    useEffect(() => {
        // questions.map((question, index) => {
        //     console.log(index, question)
        //     tests.map((test) => (
        //         console.log(test.name, test.response[index].answer)
        //     ))
        // })
        console.log(tests[0].response[0].answer)
    }, []);
    return (
        <div>
            <h2>Responses</h2>
            <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Question</TableCell>
                        {tests.map((test) => (
                            <TableCell>{test.name}</TableCell>
                        ))}
                    </TableRow>

                </TableHead>
                <TableBody>
                    {questions.map((question, index) => (
                        <TableRow key={index}>
                            <TableCell><b>{question}</b></TableCell>
                            {tests.map((test) => (
                                <TableCell key={index}>{test.response[index].answer}</TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            </TableContainer>
        </div>
    );
}

export default TestResponse2;