import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";

const Profile = () => {
  const navigate = useNavigate();
  const { isLoggedIn } = useContext(AuthContext);
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token =
      localStorage.getItem("token") || sessionStorage.getItem("token");
    if (!token) {
      setError("You need to log in to view this page. Please login first.");
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch("/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setProfileData(data);
        } else {
          localStorage.removeItem("token");
          sessionStorage.removeItem("token");
          setError("No token found. Please login first.");
        }
      } catch (err) {
        console.error("Error fetching profile:", error);
        setError("An error occurred while fetching profile data.");
      }
    };

    fetchProfile();
  }, [isLoggedIn, navigate]);

  if (!profileData) return <h2>Loading profile...</h2>;
  if (error) return <h2>Error: {error}</h2>;

  return (
    <div>
      <h1>Welcome! {profileData?.username || "User"}</h1>
    </div>
  );
};

export default Profile;
