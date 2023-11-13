import React, { useState } from "react";
import Box from "@mui/material/Box";
import { Button } from "@mui/material";
import TextField from "@mui/material/TextField";

function Question() {
  const [response, setResponse] = useState("");
  const [question, setQuestion] = useState("");
  const [reference, setReference] = useState();
  const [counter, setCounter] = useState(0);
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
        setCounter(counter + 1);
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
      <h2>Section 1/4 - Ask Questions about 2022 News</h2>
      <p>Please submit at least 3 questions. <b>The data source is CNN news from January 2022 to March 2022</b>, so please only ask about news that happen in between January 2022 to March 2022.</p>
      <p>If you don't remember what happened during that time, <a href="https://docs.google.com/document/d/1mZZ0QkbD1SOg9jsZvd73Ns-2rWq-M5LK82cekj4NTrg/edit?usp=sharing" target="_blank">check this doc!</a></p>
      
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
      { counter >= 3 && <h2>Thanks! <a href="/sample_response">Please click here to continue to next section.</a></h2>}
      <p>{`question count: ${counter}`}</p>
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
