import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { JSX } from "react/jsx-dev-runtime";

export default function ProtectedRoute({
  children,
}: {
  children: JSX.Element;
}) {
  const { accessToken } = useAuth();

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
