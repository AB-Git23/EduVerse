export interface UserProfile {
  id: number
  email: string
  username: string
  role: "student" | "instructor" | "admin"
}
