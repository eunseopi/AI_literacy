import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import SummaryPage from "./components/SummaryPage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/SignUp" element={<SignUpPage />} />
                <Route path="/Home" element={<Home />} />
                <Route path="/summary" element={<SummaryPage />} />
            </Routes>
        </Router>
    );
}

export default App;
