// a react component that displays questions and responses from responses.json
import React, { useEffect, useState } from "react";

import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import { Button } from "@mui/material";

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

function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function SampleResponse({ heading, sampleRes, mapping, nextPage, sessionId }) {
  // display one question and its response, click "next" to display the next question and response
  const [samples, setSamples] = React.useState([]);
  const [optOrders, setOptOrders] = React.useState([]);
  const [responses, setResponses] = React.useState({});
  const [isWaiting, setIsWaiting] = React.useState(false);
  const [showNext, setShowNext] = React.useState(false);
  useEffect(() => {
    let randomSamples = [];
    let orders = [];
    for (let i = 0; i < 15; i += 5) {
      const randomIndex = getRandomNumber(i, i + 4);
      const order = shuffleArray(mapping);
      randomSamples.push(randomIndex);
      orders.push(order);
    }
    setSamples(randomSamples);
    setOptOrders(orders);
  }, []);

  async function submit(e) {
    e.preventDefault();
    for (let i = 0; i < samples.length; i++) {
      if (responses[i] === undefined || responses[i]["answer"] === "") {
        alert(`Question ${i + 1} is not answered. Please select an option.`);
        return;
      }
    }
    try {
      setIsWaiting(true);
      console.log(responses);
      const res = await fetch("/log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            sessionId: sessionId,
            data: responses 
        }),
      });
      if (res.ok) {
        setIsWaiting(false);
        setShowNext(true);
      } else {
        alert("Error submitting question. Please refresh the page and try again. Sorry!");
      }
    } catch (error) {
      alert("Error submitting question. Please refresh the page and try again. Sorry!");
    }
  }
  return (
    <div>
        <h2>{heading}</h2>
        <p>Please select one response that you like/prefer for each question. You can use the text box to explain your selection.</p>
      <form onSubmit={submit}>
        {samples &&
          optOrders &&
          samples.map((sample, index) => {
            const abc = ["(A) \n", "(B) \n", "(C) \n"];
            const options = optOrders[index].map((order, i) => {
              return {
                label: abc[i] + sampleRes[order][sample].answer,
                value: order + "|" + sampleRes[order][sample].answer,
              };
            });
            return (
              <FormControl style={{ marginBottom: "30px" }}>
                <FormLabel style={{ marginBottom: "10px" }}>
                  {questions[sample]}
                </FormLabel>
                <RadioGroup
                  required
                  name="radio-buttons-group"
                  onChange={(e) => {
                    setResponses((responses) => ({
                      ...responses,
                      [index]: {
                        question: questions[sample],
                        answer: e.target.value,
                        reason: "",
                      },
                    }));
                  }}>
                  {
                    options.map((option) => {
                        return (
                            <FormControlLabel
                                value={option["value"]}
                                control={<Radio />}
                                label={option["label"]}
                                style={{ 
                                    marginBottom: "10px", backgroundColor: option.value === responses[index]?.answer ? "#e3f2fd" : "white", }}
                            />
                        )
                  })}
                </RadioGroup>
                <TextField
                  id="filled-helperText"
                  label="Why?"
                  defaultValue=""
                  helperText="Explain why you chose this answer if there is a reason."
                  variant="standard"
                  onChange={(e) => {
                    setResponses((responses) => ({
                      ...responses,
                      [index]: {
                        question: questions[sample],
                        answer: responses[index]
                          ? responses[index]["answer"]
                          : "",
                        reason: e.target.value,
                      },
                    }));
                  }}
                />
              </FormControl>
            );
          })}
          {
            showNext ? (
            <h2>
            Your response has been recorded!{" "}
            <a href={nextPage}>Please click here to go to the next section.</a>
            </h2>
        ) : (
            <Button onClick={submit} variant="contained" size="large">
            submit
            </Button>
        )
        }
      </form>
      {isWaiting && <p>Hang on, submitting your responses...</p>}
    </div>
  );
}

export default SampleResponse;
