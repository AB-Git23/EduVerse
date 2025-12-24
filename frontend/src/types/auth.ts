export interface Tokens {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  role: "student" | "instructor" | "admin";
}

export interface LoginResponse {
  access: string;
  refresh: string;
}
