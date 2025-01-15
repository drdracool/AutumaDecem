import React from "react";

const Signup = () => {
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
        const data = await response.json();
        alert(data.message);
      } else {
        const error = await response.json();
        alert(error.error);
      }
    } catch (err) {
      console.error("Error signing up", err);
    }
  };

  return (
    <div>
      <h3>Sign up</h3>
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
