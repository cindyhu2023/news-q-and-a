import React from "react";
import Question from './Question';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TestResponse from './TestResponse';

function App() {
  return (
    <div style={{width: "70%", marginLeft: "auto", marginRight: "auto"}}>
    <Router>
    <Routes>
      <Route path="/" exact element={<Question />} />
      <Route path="/test_response" element={<TestResponse />} />
     </Routes>
    </Router>
    </div>
  );
}

export default App;
