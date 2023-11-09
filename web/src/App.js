import Question from './Question';
import TestResponse from './TestResponse';
import TestResponse2 from './TestResponse2';
import SampleResponse from './SampleResponse';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/" exact element={<Question />} />
      <Route path="/test_response" element={<TestResponse />} />
      <Route path="/test_response2" element={<TestResponse2 />} />
      <Route path="/sample_response" element={<SampleResponse />} />
    </Routes>
    </Router>
    
  );
}

export default App;
