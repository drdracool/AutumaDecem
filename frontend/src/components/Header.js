import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignupModal from "./SignupModal";
import { AuthContext } from "./AuthContext";
import "./Header.css";

const Header = () => {
  const { isLoggedIn, userName, logout } = useContext(AuthContext);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);

  return (
    <header>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          {isLoggedIn ? (
            <>
              <li>
                <Link to="/profile">{userName}</Link>
              </li>
              <li>
                <button onClick={logout}>Logout</button>
              </li>
            </>
          ) : (
            <>
              <li>
                <button onClick={() => setShowLoginModal(true)}>Login</button>
              </li>
              <li>
                <button onClick={() => setShowSignupModal(true)}>Signup</button>
              </li>
            </>
          )}
        </ul>
      </nav>
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} />
      )}
      {showSignupModal && (
        <SignupModal onClose={() => setShowSignupModal(false)} />
      )}
    </header>
  );
};

export default Header;
