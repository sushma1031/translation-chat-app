"use client";
import { FormEvent, useState } from "react";
import createAPIConfig from "../config/config.js";
import { useRouter } from "next/navigation";
import Link from "next/link";
import AlertSnackbar from "../components/AlertSnackbar.tsx";
import { useDispatch } from "react-redux";
import { setToken, setUser } from "../redux/userSlice.ts";

export default function Login() {
  const [data, setData] = useState({
    email: "",
    password: ""
  });
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<"success" | "error">("error");
  const router = useRouter();
  const dispatch = useDispatch();

  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setData((prev) => {
      return {
        ...prev,
        [name]: value,
      };
    });
  };
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    e.stopPropagation();
    const apiConfig = createAPIConfig();

    try {
      const response = await apiConfig.post("login", data, {withCredentials: true});
      console.log("response", response);

      setStatus("success");
      setOpen(true);

      if (response.data.success) {
        setData({
          email: "",
          password: "",
        });
        dispatch(setToken(response?.data?.token));
        localStorage.setItem("token", response?.data?.token);

      }
      router.push("/");
    } catch (error) {
      console.log(error);
      setStatus("error");
      setOpen(true);
    }
  };
  
  return (
    <div className="w-full max-w-md rounded overflow-hidden p-4 mx-auto">
      <h1 className="text-xl text-center">Login</h1>
      <form className="grid gap-4 mt-5" onSubmit={handleSubmit}>

        <div className="flex flex-col gap-1">
          <input
            type="email"
            id="email"
            name="email"
            placeholder="Email"
            className="bg-slate-100 px-2 py-1 focus:outline-primary"
            value={data.email}
            onChange={handleOnChange}
            required
          />
        </div>

        <div className="flex flex-col gap-1">
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Password"
            className="bg-slate-100 px-2 py-1 focus:outline-primary"
            value={data.password}
            onChange={handleOnChange}
            required
          />
        </div>

        <button
          type="submit"
          className="bg-slate-300 text-lg px-4 py-1 hover:bg-slate-400 rounded mt-2 font-bold leading-relaxed tracking-wide"
        >
          Login
        </button>
      </form>

      <p className="my-3 text-center">
        New user?{" "}
        <Link
          href="/register"
          className="font-medium text-blue-600 dark:text-blue-500 hover:underline"
        >
          Register
        </Link>
      </p>
      {open && (
        <AlertSnackbar
          open={open}
          setOpen={setOpen}
          type={status}
          message={
            status === "success"
              ? "Login successful!"
              : "Incorrect username or password."
          }
        />
      )}
    </div>
  );

}