import api from "./axios";

export const registerInstructor = async (data: {
  email: string;
  username: string;
  password: string;
  bio?: string;
  expertise?: string;
  documents: File[];
}) => {
  const formData = new FormData();

  formData.append("email", data.email);
  formData.append("username", data.username);
  formData.append("password", data.password);

  if (data.bio) formData.append("bio", data.bio);
  if (data.expertise) formData.append("expertise", data.expertise);

  data.documents.forEach(file => {
    formData.append("verification_documents", file);
  });

  const response = await api.post(
    "users/register/instructor/",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};
