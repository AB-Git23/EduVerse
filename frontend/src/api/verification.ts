import api from "./axios";

export interface VerificationSubmission {
  id: number;
  status: "pending" | "approved" | "rejected";
  rejection_reason: string;
  created_at: string;
}

export interface VerificationStatusResponse {
  is_verified: boolean;
  current_submission: VerificationSubmission | null;
  can_resubmit: boolean;
}

export const getVerificationStatus = async (): Promise<VerificationStatusResponse> => {
  const res = await api.get<VerificationStatusResponse>(
    "users/instructor/verification/status/"
  );
  return res.data;
};

export const submitVerification = async (files: File[]) => {
  const formData = new FormData();
  files.forEach((file) =>
    formData.append("verification_documents", file)
  );

  await api.post(
    "users/instructor/verification/submit/",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );
};
