import api from "./axios";

export const fetchProfile = async () => {
  const response = await api.get("users/profile/");
  return response.data;
};

export const updateProfile = async (data: any) => {
  const response = await api.put("users/profile/", data);
  return response.data;
};
