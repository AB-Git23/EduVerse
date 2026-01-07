import { useEffect, useState } from "react";
import { getPendingSubmissions } from "../../api/admin";

export default function VerificationList() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPendingSubmissions().then((res) => {
      setItems(res.results ?? res);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading submissions…</p>;

  return (
    <>
      <h2>Pending Instructor Verifications</h2>

      {items.length === 0 && <p>No pending submissions.</p>}

      <ul>
        {items.map((item) => (
          <li key={item.id}>
            {item.instructor_email} —{" "}
            <a href={`/admin/verification/${item.id}`}>Review</a>
          </li>
        ))}
      </ul>
    </>
  );
}
