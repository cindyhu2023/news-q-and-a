// a react component that displays questions and responses from responses.json
import React, { useState, useEffect } from 'react';
// import data from './test_response/responses.json';
import test1 from './test_response/responses.json';
import test2 from './test_response/responses_reader_roberta-base-squad2.json';
import test3 from './test_response/responses_retriever_reader.json';
import test4 from './test_response/responses_reader_distilled.json';
import test5 from './test_response/responses_open_ai.json';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Tab } from '@mui/material';

const tests = [
    {
        "name": "test1",
        "retriever": "plain retriever",
        "top_k": 3,
        "query_model": "open ai - text-davinci-003",
        "response": test1
    },
    {
        "name": "test2",
        "retriever": "plain retriever",
        "top_k": 10,
        "query_model": "reader - roberta-base-squad2",
        "response": test2
    },
    {
        "name": "test3",
        "retriever": "embedding retriever - multi-qa-mpnet-base-dot-v1",
        "top_k": 10,
        "query_model": "reader - roberta-base-squad2",
        "response": test3
    },
    {
        "name": "test4",
        "retriever": "embedding retriever - multi-qa-mpnet-base-dot-v1",
        "top_k": 10,
        "query_model": "reader - distilbert-base-uncased-distilled-squad",
        "response": test4
    },
    {
        "name": "test5",
        "retriever": "embedding retriever - multi-qa-mpnet-base-dot-v1",
        "top_k": 5,
        "query_model": "open ai - text-davinci-003",
        "response": test5
    }

]

const questions = [
    "What's the damage of Colorado wildfire?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What's the number of COVID-19 cases in the US?",
    "How many people died from COVID-19 in the US?",
    "What is the new COVID-19 variant?",
    "Is Moderna vaccine allowed for children?",
    "Did the US send troops to Ukraine?",
    "What is Truth Social?",
    "Who uses Truth Social?",
    "Who is the first black woman in Supreme Court?",
    "Who is Ketanji Jackson?",
    "Is the inflation bad in the US?",
    "What is the inflation rate in the US?",
    "How much was Twitter sold for?",
    "Why did Elon Musk buy Twitter?",
    "What is Roe v. Wade?",
    "What is the new abortion law in Texas?",
    "Why is Roe v. Wade controversial?",
    "What damage did Hurricane Ian cause?",
    "How many medals did the US win in the 2022 Winter Olympics?",
    "Is Queen Elizabeth dead?",
]


function TestResponse() {
    return (
        <div>
            <h2>Responses</h2>
            <div>
                {
                    tests.map((test) => (
                        <div>
                            <h3>{test.name}</h3>
                            <ul>
                            <li>retriever: {test.retriever}</li>
                            <li>top_k: {test.top_k}</li>
                            <li>query_model: {test.query_model}</li>
                            </ul>
                            
                        </div>
                    ))
                }
            </div>
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

export default TestResponse;