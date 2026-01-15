import { useEffect, useState } from "react";
import { useAuth } from "../../auth/AuthContext";
import { getInstructorCourses } from "../../api/courses";

export default function InstructorDashboard() {
  const { user } = useAuth();
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getInstructorCourses()
      .then(setCourses)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading dashboard…</p>;

  return (
    <>
      <h2>Instructor Dashboard</h2>

      <p>
        Status:{" "}
        {user?.is_verified ? "Verified" : "Not verified"}
      </p>

      <button disabled={!user?.is_verified}>
        Create Course
      </button>

      <h3>Your Courses</h3>

      {courses.length === 0 && <p>No courses yet.</p>}

      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            {course.title} —{" "}
            {course.is_published ? "Published" : "Draft"}
          </li>
        ))}
      </ul>
    </>
  );
}
