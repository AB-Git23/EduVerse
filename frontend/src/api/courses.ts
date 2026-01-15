import api from "./axios";

export interface InstructorCourse {
  id: number;
  title: string;
  description: string;
  is_published: boolean;
  created_at: string;
}

export const getInstructorCourses = async () => {
  const res = await api.get("courses/instructor/courses/");
  return res.data;
};

export const createCourse = async (
  title: string,
  description: string
) => {
  const res = await api.post("courses/instructor/courses/", {
    title,
    description,
  });
  return res.data;
};
