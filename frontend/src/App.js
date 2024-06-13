import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import SummaryPage from "./components/SummaryPage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import Profile from "./pages/Profile";
import Summaries from "./pages/Summaries";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/SignUp" element={<SignUpPage />} />
                <Route path="/Home" element={<Home />} />
                <Route path="/summary" element={<SummaryPage />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/summaries" element={<Summaries />} />
            </Routes>
        </Router>
    );
}

export default App;
