import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import ProtectedRoute from "./auth/ProtectedRoute";
import Verification from "./pages/Verification";
import RegisterInstructor from "./pages/RegisterInstructor";
import VerificationList from "./pages/admin/VerificationList";
import VerificationDetail from "./pages/admin/VerificationDetail";



function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register/instructor" element={<RegisterInstructor />} />

        <Route
          path="/admin/verification"
          element={
            <ProtectedRoute>
              <VerificationList />
            </ProtectedRoute>
          }
        />

          <Route
          path="/admin/verification/:id"
          element={
            <ProtectedRoute>
              <VerificationDetail />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/verification"
          element={
            <ProtectedRoute>
              <Verification />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}


export default App;
