import { useState } from "react";
import { registerInstructor } from "../api/register";

export default function RegisterInstructor() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [bio, setBio] = useState("");
  const [expertise, setExpertise] = useState("");
  const [documents, setDocuments] = useState<File[]>([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // ✅ Incremental add logic
  const handleAddFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const newFiles = Array.from(e.target.files);
    setDocuments(prev => [...prev, ...newFiles]);

    // reset input so user can add again
    e.target.value = "";
  };

  const removeFile = (index: number) => {
    setDocuments(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (documents.length === 0) {
      setError("Verification documents are required.");
      return;
    }

    try {
      await registerInstructor({
        email,
        username,
        password,
        bio,
        expertise,
        documents,
      });
      setSuccess("Instructor registered. Verification pending.");
    } catch (err) {
      setError("Registration failed.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Instructor Registration</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />

      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />

      <textarea
        placeholder="Bio"
        value={bio}
        onChange={e => setBio(e.target.value)}
      />

      <input
        placeholder="Expertise"
        value={expertise}
        onChange={e => setExpertise(e.target.value)}
      />

      {/* ✅ Incremental file picker */}
      <div>
        <label>
          Add verification documents
          <input
            type="file"
            multiple
            onChange={handleAddFiles}
            style={{ display: "block", marginTop: "8px" }}
          />
        </label>

        {documents.length > 0 && (
          <ul>
            {documents.map((file, index) => (
              <li key={index}>
                {file.name}
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  style={{ marginLeft: "10px" }}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <button type="submit">Register as Instructor</button>
    </form>
  );
}
