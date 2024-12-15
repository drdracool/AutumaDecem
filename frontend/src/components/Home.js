import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [titles, setTitles] = useState([]);
  useEffect(() => {
    fetch("/titles")
      .then((res) => res.json())
      .then((data) => {
        setTitles(data);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Titles</h1>
        <ul>
          {titles.map((item, index) => {
            console.log(item);
            return (
              <li key={index}>
                <Link to={`/post/${item.slug}`}>{item.title}</Link>
              </li>
            );
          })}
        </ul>
      </header>
    </div>
  );
}

export default Home;
