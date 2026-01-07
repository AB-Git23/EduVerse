import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { JSX } from "react/jsx-runtime";

export default function AdminRoute({
  children,
}: {
  children: JSX.Element;
}) {
  const { isAuthenticated, isLoading, role } = useAuth();

  if (isLoading) return null;

  if (!isAuthenticated || role !== "admin") {
    return <Navigate to="/login" replace />;
  }

  return children;
}
