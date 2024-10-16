import axios from "axios";
const createAPIConfig = () => {
  const instance = axios.create({
    baseURL: "http://localhost:5328/api/",
  });
  return instance;
};

export default createAPIConfig;
