// a react component that displays questions and responses from responses.json
import React, { useEffect } from 'react';
// import data from './test_response/responses.json';
import sample1 from './samples/sample_response_1.json';
import sample2 from './samples/sample_response_2.json';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const test1 = [
    {
        "name": "default",
        "response": sample1["default"]
    },
    {
        "name": "long",
        "response": sample1["long"]
    },
    {
        "name": "short",
        "response": sample1["short"]
    }
]

const test2 = [
    {
        "name": "temperature_0.1",
        "response": sample2["temperature_0.1"]
    },
    {
        "name": "temperature_0.5",
        "response": sample2["temperature_0.5"]
    },
    {
        "name": "temperature_0.9",
        "response": sample2["temperature_0.9"]
    }
]

const questions = [
    //0-5
    "Can pig hearts be used for human transplants?",
    "Why did the man receive a pig heart transplant?",
    "Why is Elizabeth Holmes on trial?",
    "Is Elizabeth Holmes guilty?",
    "What was the Supreme Court's ruling on the Biden administration's vaccine mandate for large employers?",
    //6-10
    "What companies took action against Russia?",
    "What is the US's stance on the Ukraine crisis?",
    "What is China's stance on the Ukraine crisis?",
    "Did the US send troops to Ukraine?",
    "Why are companies are moving out of Russia?",
    //11-15
    "Who's nominated for best supporting actress?",
    "Who is Ketanji Jackson?",
    "What's the controversy surrounding Eileen Gu?",
    "Who is Eileen Gu?",
    "What images did James Webb Telescope capture?",
  ];

function TestResponse() {
    return (
        <div style={{width: "100%"}}>
            <h2>Responses - group 1</h2>
            <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Question</TableCell>
                        {test1.map((test) => (
                            <TableCell>{test.name}</TableCell>
                        ))}
                    </TableRow>

                </TableHead>
                <TableBody>
                    {questions.map((question, index) => (
                        <TableRow key={index}>
                            <TableCell><b>{question}</b></TableCell>
                            {test1.map((test) => (
                                <TableCell key={index}>{test.response[index].answer}</TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            </TableContainer>

            <h2>Responses - group 2</h2>
            <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Question</TableCell>
                        {test2.map((test) => (
                            <TableCell>{test.name}</TableCell>
                        ))}
                    </TableRow>

                </TableHead>
                <TableBody>
                    {questions.map((question, index) => (
                        <TableRow key={index}>
                            <TableCell><b>{question}</b></TableCell>
                            {test2.map((test) => (
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