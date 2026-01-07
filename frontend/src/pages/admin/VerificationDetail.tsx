import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  getSubmissionDetail,
  approveSubmission,
  rejectSubmission,
} from "../../api/admin";
import type { AdminSubmissionDetail } from "../../types/admin";

export default function VerificationDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<AdminSubmissionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [rejectReason, setRejectReason] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = async () => {
    if (!id) return;
    const res = await getSubmissionDetail(Number(id));
    setData(res);
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, [id]);

  const handleApprove = async () => {
    if (!id) return;
    setSubmitting(true);
    await approveSubmission(Number(id));
    navigate("/admin/verification");
  };

  const handleReject = async () => {
    if (!id || !rejectReason) return;
    setSubmitting(true);
    await rejectSubmission(Number(id), rejectReason);
    navigate("/admin/verification");
  };

  if (loading) return <p>Loading submission…</p>;
  if (!data) return <p>Submission not found.</p>;

  return (
    <>
      <h2>Verification Submission</h2>

      <p>
        <strong>Instructor:</strong>{" "}
        {data.instructor_username} ({data.instructor_email})
      </p>

      <p>
        <strong>Status:</strong> {data.status}
      </p>

      <p>
        <strong>Submitted:</strong>{" "}
        {new Date(data.created_at).toLocaleString()}
      </p>

      <h3>Documents</h3>
      <ul>
        {data.documents.map((doc) => (
          <li key={doc.id}>
            <a href={doc.document} target="_blank" rel="noreferrer">
              View document
            </a>
          </li>
        ))}
      </ul>

      {data.status === "pending" && (
        <>
          <hr />

          <button onClick={handleApprove} disabled={submitting}>
            Approve
          </button>

          <br /><br />

          <textarea
            placeholder="Rejection reason"
            value={rejectReason}
            onChange={(e) => setRejectReason(e.target.value)}
          />

          <br />

          <button
            onClick={handleReject}
            disabled={submitting || !rejectReason}
          >
            Reject
          </button>
        </>
      )}
    </>
  );
}
