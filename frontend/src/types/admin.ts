export interface VerificationDocument {
  id: number;
  document: string;
  uploaded_at: string;
}

export interface AdminSubmissionDetail {
  id: number;
  status: "pending" | "approved" | "rejected";
  rejection_reason: string;
  created_at: string;
  reviewed_at: string | null;
  instructor_email: string;
  instructor_username: string;
  documents: VerificationDocument[];
}
