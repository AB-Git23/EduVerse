import { useEffect, useState } from "react";
import { fetchProfile } from "../api/profile";

export default function Profile() {
  const [profile, setProfile] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProfile()
      .then(data => setProfile(data))
      .catch(() => setError("Failed to load profile"));
  }, []);

  if (error) return <p>{error}</p>;
  if (!profile) return <p>Loading...</p>;

  return (
    <div>
      <h2>Profile</h2>
      <pre>{JSON.stringify(profile, null, 2)}</pre>
    </div>
  );
}
