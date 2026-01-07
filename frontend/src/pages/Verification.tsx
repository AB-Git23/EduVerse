import { useEffect, useState } from "react";
import {
  getVerificationStatus,
  submitVerification,
  type VerificationStatusResponse,
} from "../api/verification";

export default function VerificationPage() {
  const [data, setData] = useState<VerificationStatusResponse | null>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const loadStatus = async () => {
    setLoading(true);
    const res = await getVerificationStatus();
    setData(res);
    setLoading(false);
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleSubmit = async () => {
    if (!files.length) return;

    setSubmitting(true);
    await submitVerification(files);
    setFiles([]);
    await loadStatus();
    setSubmitting(false);
  };

  if (loading) return <p>Loading verification status…</p>;
  if (!data) return <p>Unable to load status.</p>;

  // VERIFIED
  if (data.is_verified) {
    return <h2>✅ You are a verified instructor</h2>;
  }

  // PENDING
  if (data.current_submission?.status === "pending") {
    return (
      <>
        <h2>⏳ Verification under review</h2>
        <p>Your documents are being reviewed.</p>
      </>
    );
  }

  // REJECTED
  if (data.current_submission?.status === "rejected") {
    return (
      <>
        <h2>❌ Verification rejected</h2>
        <p>
          <strong>Reason:</strong>{" "}
          {data.current_submission.rejection_reason}
        </p>
        {data.can_resubmit && renderUpload()}
      </>
    );
  }

  // NO SUBMISSION YET
  return (
    <>
      <h2>Submit verification documents</h2>
      {renderUpload()}
    </>
  );

  function renderUpload() {
    return (
      <>
        <input
          type="file"
          multiple
          onChange={(e) =>
            setFiles(Array.from(e.target.files ?? []))
          }
        />
        <br />
        <button
          onClick={handleSubmit}
          disabled={submitting || files.length === 0}
        >
          {submitting ? "Submitting…" : "Submit"}
        </button>
      </>
    );
  }
}
