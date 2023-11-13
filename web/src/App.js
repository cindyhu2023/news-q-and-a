import React, { useState } from "react";
import Question from './Question';
import SampleResponse from './SampleResponse';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import sampleRes1 from './samples/sample_response_1.json';
import sampleRes2 from './samples/sample_response_2.json';

const sample1Mapping = [
   "default",
   "short",
   "long"
]

const sample2Mapping = [
  "temperature_0.5",
  "temperature_0.9",
  "temperature_0.1"
]

function generateRandomString() {
  const alphanumeric = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let randomString = '';

  for (let i = 0; i < 8; i++) {
    const randomIndex = Math.floor(Math.random() * alphanumeric.length);
    randomString += alphanumeric.charAt(randomIndex);
  }

  return randomString;
}

function App() {
  const [sessionId, _] = useState(generateRandomString());
  return (
    <div style={{width: "70%", marginLeft: "auto", marginRight: "auto"}}>
    <Router>
    <Routes>
      <Route path="/" exact element={<Question />} />
      {/* <Route path="/test_response" element={<TestResponse />} />
      <Route path="/test_response2" element={<TestResponse2 />} />
      <Route path="/test_response3" element={<TestResponse3 />} /> */}
      <Route path="/sample_response" element={<SampleResponse heading="Section 2/4" sampleRes={sampleRes1} mapping={sample1Mapping} nextPage="/sample_response2" sessionId={sessionId}/>} />
      <Route path="/sample_response2" element={<SampleResponse heading="Section 3/4" sampleRes={sampleRes2} mapping={sample2Mapping} nextPage="https://forms.gle/BhEYBWh7cN4zeUJ87" sessionId={sessionId}/>} />
    </Routes>
    </Router>
    </div>
  );
}

export default App;
