// a react component that displays questions and responses from responses.json
import React, { useEffect } from 'react';
// import data from './test_response/responses.json';
import test1 from './test_response_3/response_length_standard.json';
import test2 from './test_response_3/response_length_short.json';
import test3 from './test_response_3/response_length_long.json'; 
import test4 from './test_response_3/response_tone_standard.json';
import test5 from './test_response_3/response_tone_casual.json';
import test6 from './test_response_3/response_tone_general_public.json';

import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const tests1 = [
    {
        "name": "response_length_standard",
        "response": test1
    },
    {
        "name": "response_length_short",
        "response": test2
    },
    {
        "name": "response_length_long",
        "response": test3
    }

]

const tests2 = [
    {
        "name": "response_tone_standard",
        "response": test4
    },
    {
        "name": "response_tone_casual",
        "response": test5
    },
    {
        "name": "response_tone_general_public",
        "response": test6
    }
]

const questions = [
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


function TestResponse3() {
    return (
        <div>
            <h2>Test group 1 - response length</h2>
            <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Question</TableCell>
                        {tests1.map((test) => (
                            <TableCell>{test.name}</TableCell>
                        ))}
                    </TableRow>

                </TableHead>
                <TableBody>
                    {questions.map((question, index) => (
                        <TableRow key={index}>
                            <TableCell><b>{question}</b></TableCell>
                            {tests1.map((test) => (
                                <TableCell key={index}>{test.response[index].answer}</TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            </TableContainer>
            <h2>Test group 2 - response tone</h2>
            <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Question</TableCell>
                        {tests2.map((test) => (
                            <TableCell>{test.name}</TableCell>
                        ))}
                    </TableRow>

                </TableHead>
                <TableBody>
                    {questions.map((question, index) => (
                        <TableRow key={index}>
                            <TableCell><b>{question}</b></TableCell>
                            {tests2.map((test) => (
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

export default TestResponse3;