import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import { Button } from '@mui/material';
import TextField from '@mui/material/TextField';

function Question() {
    const [response, setResponse] = useState('');
    const [question, setQuestion] = useState('');
    const [reference, setReference] = useState();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });
            if (response.ok) {
                const jsonResponse = await response.json();
                setResponse(jsonResponse.answer);
                setReference(jsonResponse.reference);
            } else {
                console.error('Error submitting question.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h2>Ask a Question</h2>
            <Box
                component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}
                noValidate
                autoComplete="off"
            >
                <TextField 
                    id="outlined-basic" 
                    label="Question" 
                    variant="outlined" 
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Type your question here"
                    rows={4}
                />
                
            </Box>
            <Button variant="contained" onClick={handleSubmit} size="small">Submit</Button>
            {question && <div>
                <h2>Question: </h2>
                <p>{question}</p>
            </div>
            }
            {response && <div>
                <h2>Response: </h2>
                <p>{response}</p>
            </div>
            }
            {reference && <div>
                <h2>Reference: </h2>
                {<div>
                {Object.keys(reference).map((key) => (
                    <p key={key}>
                    [{key}] {<a href={reference[key]}>{reference[key]}</a>}
                    </p>
                ))}
                </div>
                }
                </div>
            }
        </div>
    );
}

export default Question;
