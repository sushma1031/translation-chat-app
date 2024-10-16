import axios from "axios";
export const createAPIConfig = () => {
  const instance = axios.create(
    {
      baseURL: "http://localhost:5328/api/",
    },
  );
  return instance;
};
