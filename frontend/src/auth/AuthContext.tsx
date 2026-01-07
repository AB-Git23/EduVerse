import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import api from "../api/axios";
import { fetchProfile } from "../api/profile";
import type { UserProfile } from "../types/profile";
import type { LoginResponse } from "../types/auth";

interface AuthContextType {
  user: UserProfile | null;
  role: UserProfile["role"] | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;
  const role = user?.role ?? null;

  const refreshProfile = async () => {
    try {
      const profile = await fetchProfile();
      setUser(profile);
    } catch {
      logout();
    }
  };

  const login = async (email: string, password: string) => {
    const res = await api.post<LoginResponse>("auth/jwt/create/", {
      email,
      password,
    });

    localStorage.setItem("accessToken", res.data.access);
    localStorage.setItem("refreshToken", res.data.refresh);

    await refreshProfile();
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
  };

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setIsLoading(false);
      return;
    }

    refreshProfile().finally(() => setIsLoading(false));
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        role,
        isAuthenticated,
        isLoading,
        login,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
};
