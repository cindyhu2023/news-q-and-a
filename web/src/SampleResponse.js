// a react component that displays questions and responses from responses.json
import React, { useEffect } from 'react';
// import data from './test_response/responses.json';
import test1 from './test_response_2/plain_3_openai.json';
import test2 from './test_response_2/embedding_5_openai.json';
import test3 from './test_response_2/embedding_3_openai.json'; 

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';

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

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

function SampleResponse(){
    // display one question and its response, click "next" to display the next question and response
    const [index, setIndex] = React.useState(0);
    const [samples, setSamples] = React.useState([]);
    const [responses, setResponses] = React.useState({});
    useEffect(() => {
        let randomSamples = [];
        for (let i = 0; i < 14; i += 5) {
            const randomIndex = getRandomNumber(i, i + 4);
            randomSamples.push(randomIndex);
        }
        setSamples(randomSamples);
        console.log(randomSamples);
    }, []);


    function submit(e){
        e.preventDefault();
        console.log(responses);
    }
    return (
        <div>
         <form onSubmit={submit}>
        { samples.map((sample, index) => { return (
            <FormControl>
            <FormLabel>{questions[sample]}</FormLabel>
            <RadioGroup
                required
                name="radio-buttons-group"
                onChange={(e) => {
                    setResponses(responses => ({...responses, [index]: {"question": questions[sample], "answer": e.target.value}, "reason": ""}));
                }}
            >
                <FormControlLabel value={tests[0].response[sample].answer} control={<Radio />} label={tests[0].response[sample].answer} />
                <FormControlLabel value={tests[1].response[sample].answer} control={<Radio />} label={tests[1].response[sample].answer} />
                <FormControlLabel value={tests[2].response[sample].answer} control={<Radio />} label={tests[2].response[sample].answer} />
            </RadioGroup>
            <TextField
                id="filled-helperText"
                label="Why?"
                defaultValue=""
                helperText="Explain why you chose this answer if there is a reason."
                variant="standard"
                onChange={(e) => {
                    setResponses(responses => ({...responses, 
                    [index]: {
                        "question": questions[sample], 
                        "answer": responses[index] ? responses[index]["answer"] : "",
                        "reason": e.target.value
                    }}));
                }}
            />
            <Button onClick={() => setIndex((index + 1) % samples.length)}>back</Button>
        {
            index === questions.length - 1 
            ? <Button onClick={submit}>submit</Button> 
            : <Button onClick={() => setIndex((index + 1) % samples.length)}>next</Button>
        }
        </FormControl>
        )})}
        </form>
        </div>
    )

}

export default SampleResponse;
