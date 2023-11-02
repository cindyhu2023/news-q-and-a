import Question from './Question';
import TestResponse from './TestResponse';
import { BrowserRouter as Router, Route, Switch, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/" exact element={<Question />} />
      <Route path="/test_response" element={<TestResponse />} />
    </Routes>
    </Router>
    
  );
}

export default App;
