import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const ActivateAccount = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  useEffect(() => {
    const activate = async () => {
      try {
        const response = await fetch(`/activate/${token}`);
        const data = await response.json();

        if (response.ok) {
          setMessage(data.message);
          setTimeout(() => navigate("/login"), 3000);
        } else {
          setMessage(data.error);
        }
      } catch (error) {
        setMessage("An error occurred.");
      }
    };

    activate();
  }, [token, navigate]);

  return <h2>{message}</h2>;
};

export default ActivateAccount;
