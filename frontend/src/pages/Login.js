import React from "react";

const Login = () => {
  return (
    <div>
      <h3>Login</h3>
      <div>
        <form method="POST" action="/login">
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
