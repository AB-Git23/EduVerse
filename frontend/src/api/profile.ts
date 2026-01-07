import api from "./axios";
import type { UserProfile } from "../types/profile";

export const fetchProfile = async (): Promise<UserProfile> => {
  const res = await api.get<UserProfile>("users/profile/");
  return res.data;
};
