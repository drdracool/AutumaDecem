import React from "react";

const Signup = () => {
  return (
    <div>
      <h3>Sign up</h3>
      <div>
        <form method="POST" action="/signup">
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
