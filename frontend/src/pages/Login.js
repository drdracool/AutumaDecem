import React from "react";

const Login = () => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    const remember = e.target.remember.checked;

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
        console.error("Error response from server:", errorText);
        alert("Login failed. Please try again.");
        return;
      }

      const data = await response.json();
      localStorage.setItem("token", data.token);
      alert("Login successful!");
    } catch (err) {
      console.error("Error logging in", err);
      alert("An unexpected error occurred.");
    }
  };

  return (
    <div>
      <h3>Login</h3>
      <div>
        <form onSubmit={handleSubmit}>
          {/* useActionState is used to update state based on the result of a form action. */}
          <div>
            <div>
              <input
                className="input"
                type="email"
                name="email"
                placeholder="Your Email"
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
                placeholder="Your Password"
              />
            </div>
          </div>
          <div>
            <label className="checkbox">
              <input type="checkbox" name="remember" />
              Remember me
            </label>
          </div>
          <button className="button">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
