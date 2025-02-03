import React, { useState, useEffect } from "react";

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("No token found. Please login first.");
        setLoading(false);
        return;
      }

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
          const errorData = await response.json();
          setError(errorData.message || "Failed to fetch profile.");
        }
      } catch (err) {
        setError("An error occurred while fetching profile data.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <h2>Loading profile...</h2>;
  if (error) return <h2>Error: {error}</h2>;

  return (
    <div>
      <h1>Welcome! {profileData.name}</h1>
    </div>
  );
};

export default Profile;
