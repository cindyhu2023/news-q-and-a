import React, { useState } from "react";
import Box from "@mui/material/Box";
import { Button } from "@mui/material";
import TextField from "@mui/material/TextField";

function Question() {
  const [response, setResponse] = useState("");
  const [question, setQuestion] = useState("");
  const [reference, setReference] = useState();
  const [isWaiting, setIsWaiting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question) {
        alert("Please enter a question.");
        return;
        }
    try {
      setIsWaiting(true);
      const response = await fetch("/question", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
      if (response.ok) {
        const jsonResponse = await response.json();
        setResponse(jsonResponse.answer);
        setReference(jsonResponse.reference);
        setIsWaiting(false);
      } else {
        setIsWaiting(false);
        alert("Error submitting question. Please refresh the page and try again. Sorry!");
      }
    } catch (error) {
      console.error("Error:", error);
      setIsWaiting(false);
      alert("Error submitting question. Please refresh the page and try again. Sorry!");
    }
  };

  return (
    <div>
      <h2>Ask anything</h2>
      <p>Note: This app is a prototype. <b>The data source is CNN news from January 2022 to March 2022.</b> If your question is about news that happened outside of that time frame, you may not be able to get an answer.</p>
      <p>Here is <a href="https://docs.google.com/document/d/1mZZ0QkbD1SOg9jsZvd73Ns-2rWq-M5LK82cekj4NTrg/edit?usp=sharing" target="_blank">the news highlight from January 2022 to March 2022</a>!</p>
      
      <Box
        component="form"
        noValidate
        autoComplete="off">
        <TextField
          id="outlined-basic"
          label="Question"
          variant="outlined"
          fullWidth
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question here"
          rows={4}
          style={{ marginBottom: "10px" }}
        />
      </Box>
      <Button variant="contained" onClick={handleSubmit} size="large" style={{marginBottom: "20px"}}>
        Submit
      </Button>
      {question && (
        <div>
          <h3>Question: </h3>
          <p>{question}</p>
        </div>
      )}
      {isWaiting ? (
        <p>Waiting for response...</p>
      ) : (
        <div>
          {response && (
            <div>
              <h3>Response: </h3>
              <p>{response}</p>
            </div>
          )}
          {reference && (
            <div>
              <h3>Reference: </h3>
              {
                <div>
                  {Object.keys(reference).map((key) => (
                    <p key={key}>
                      [{key}] {<a href={reference[key]}>{reference[key]}</a>}
                    </p>
                  ))}
                </div>
              }
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Question;
