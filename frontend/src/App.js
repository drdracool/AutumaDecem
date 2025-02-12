import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./components/Home";
import Post from "./components/Post";
import Header from "./components/Header";
import Profile from "./pages/Profile";
import ActivateAccount from "./pages/ActivateAccount";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/post/:slug" element={<Post />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/activate/:token" element={<ActivateAccount />} />
      </Routes>
    </Router>
  );
}

export default App;
