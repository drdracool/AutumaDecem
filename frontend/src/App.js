import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [titles, setTitles] = useState([]);
  useEffect(() => {
    fetch("/titles").then((res) =>
      res.json().then((data) => {
        setTitles(data);
      })
    );
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Titles</h1>
        <ul>
          {titles.map((item, index) => {
            <li key={index}>{item.title}</li>;
          })}
        </ul>
      </header>
    </div>
  );
}

export default App;
