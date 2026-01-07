import { useAuth } from "../auth/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const { isAuthenticated, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={{ marginBottom: "20px" }}>
      {isAuthenticated && (
        <>
          <Link to="/profile">Profile</Link>{" | "}

          {role === "instructor" && (
            <>
              <Link to="/verification">Verification</Link>{" | "}
            </>
          )}

          {role === "student" && (
            <>
              <Link to="/register/instructor">
                Register as Instructor
              </Link>{" | "}
            </>
          )}

          {role === "admin" && (
            <>
              <Link to="/admin/verification">
                Admin Dashboard
              </Link>{" | "}
            </>
          )}

          <button onClick={handleLogout}>Logout</button>
        </>
      )}

      {!isAuthenticated && (
        <>
          <Link to="/login">Login</Link>
        </>
      )}
    </nav>
  );
}
