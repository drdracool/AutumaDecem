import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import { AuthContext } from "./AuthContext";
import "./Header.css";

const Header = () => {
  const { isLoggedIn, userName, logout } = useContext(AuthContext);
  const [showLoginModal, setShowLoginModal] = useState(false);

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
                <Link to="/signup">Signup</Link>
              </li>
            </>
          )}
        </ul>
      </nav>
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} />
      )}
    </header>
  );
};

export default Header;
