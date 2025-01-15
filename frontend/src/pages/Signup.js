import { useState } from "react";
import React from "react";

const Signup = () => {
  const [notification, setNotification] = useState(null);
  const [notificationType, setNotificationType] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    const username = e.target.username.value;

    try {
      const response = await fetch("/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, username }),
      });

      if (response.ok) {
        setNotification("Registration successful! Please log in.");
        setNotificationType("success");
        e.target.reset();
      } else {
        const error = await response.json();
        setNotification(error.error || "An error occurred.");
        setNotificationType("error");
      }
    } catch (err) {
      console.error("Error signing up", err);
      setNotification("An unexpected error occurred.");
      setNotificationType("error");
    }

    // setTimeout(() => {
    //   setNotification(null);
    //   setNotificationType("");
    // }, 5000);
  };

  return (
    <div>
      <h3>Sign up</h3>
      {notification && (
        <div
          className={`flash-message ${
            notificationType === "success" ? "flash-success" : "flash-error"
          }`}
        >
          {notification}
        </div>
      )}
      <div>
        <form onSubmit={handleSubmit}>
          <div>
            <div>
              <input
                className="input"
                type="email"
                name="email"
                placeholder="Email"
                autoFocus=""
              />
            </div>
          </div>
          <div>
            <div>
              <input
                className="input"
                type="text"
                name="username"
                placeholder="Username"
                autoFocus=""
              />
            </div>
          </div>
          <div>
            <div>
              <input
                className="input"
                type="password"
                name="password"
                placeholder="Password"
              />
            </div>
          </div>
          <button className="button">Sign up</button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
