import React, { useState } from "react";

const LoginModal = ({ onClose, onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [remember, setRemember] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request to the /login endpoint with the user's information
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, remember }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        setError(errorText);
        return;
      }

      const data = await response.json();
      localStorage.setItem("token", data.token);
      localStorage.setItem("userName", data.username);
      onLogin(data.username);
      onClose();
    } catch (err) {
      setError("Error logging in");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Login</h3>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          {/* useActionState is used to update state based on the result of a form action. */}
          <input
            className="input"
            type="email"
            name="email"
            placeholder="Your Email"
            autoFocus=""
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            className="input"
            type="password"
            name="password"
            placeholder="Your Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <div>
            <label className="checkbox">
              <input type="checkbox" name="remember" />
              Remember me
            </label>
          </div>
          <button type="submit">Login</button>
        </form>
        <button onClick={onClose} className="close-button">
          Close
        </button>
      </div>
    </div>
  );
};

export default LoginModal;
