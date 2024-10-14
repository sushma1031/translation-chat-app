import axios, { AxiosInstance } from "axios";
export const createApiConfig = () => {
  const instance = axios.create(
    {
      baseURL: "http://localhost:5328/api/",
    },
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  return instance;
};
