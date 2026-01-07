import api from "./axios";

export interface AdminSubmission {
  id: number;
  status: "pending" | "approved" | "rejected";
  created_at: string;
  instructor_email: string;
}

export const getPendingSubmissions = async () => {
  const res = await api.get("users/admin/verification-submissions/?status=pending");
  return res.data;
};

export const getSubmissionDetail = async (id: number) => {
  const res = await api.get(`users/admin/verification-submissions/${id}/`);
  return res.data;
};

export const approveSubmission = async (id: number) => {
  await api.post(`users/admin/verification-submissions/${id}/approve/`);
};

export const rejectSubmission = async (id: number, reason: string) => {
  await api.post(`users/admin/verification-submissions/${id}/reject/`, {
    rejection_reason: reason,
  });
};

export const getAuditLog = async (id: number) => {
  const res = await api.get(`users/admin/verification-submissions/${id}/audit/`);
  return res.data;
};
