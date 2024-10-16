"use client";
import { FormEvent, useState } from "react";
import { createAPIConfig } from "../config/config.js";
import AlertSnackbar from "../components/AlertSnackbar.tsx"; 
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Register() {
  const [data, setData] = useState({
    name: "",
    email: "",
    password: "",
    profile_pic: "",
    language: "english"
  });
  const [uploadPhoto, setUploadPhoto] = useState("");
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<"success" | "error">("error")
  const router = useRouter();

  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setData((prev) => {
      return {
        ...prev,
        [name]: value,
      };
    });
  };

  const handleUploadPhoto = async (e: React.ChangeEvent<HTMLInputElement>) => {
    // const file = e.target.files[0];

    const uploadPhoto = { todo: "upload to Cloudinary", url: "" };

    // setUploadPhoto(file);

    setData((prev) => {
      return {
        ...prev,
        profile_pic: uploadPhoto?.url,
      };
    });
  };

  const handleClearUploadPhoto = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.stopPropagation();
    e.preventDefault();
    setUploadPhoto("");
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    e.stopPropagation();
    const apiConfig = createAPIConfig();

    try {
      const response = await apiConfig.post("register", data);
      console.log("response", response);
      
      setStatus("success");
      setOpen(true);

      if (response.data.success) {
        setData({
          name: "",
          email: "",
          password: "",
          profile_pic: "",
          language: "",
        });
      }
      router.push("/login");
    } catch (error) {
      console.log(error);
      setStatus("error");
      setOpen(true);
    }
    console.log("data", data);
  };

  return (
    <div className="w-full max-w-md rounded overflow-hidden p-4 mx-auto">
      <h1 className="text-xl text-center">Register</h1>
      <form className="grid gap-4 mt-5" onSubmit={handleSubmit}>
        <div className="flex flex-col gap-1">
          <input
            type="text"
            id="name"
            name="name"
            placeholder="Name"
            className="bg-slate-100 px-2 py-1 focus:outline-primary"
            value={data.name}
            onChange={handleOnChange}
            required
          />
        </div>

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
        <div className="flex flex-col gap-1">
          <input
            type="text"
            id="language"
            name="language"
            placeholder="Preferred language"
            className="bg-slate-100 px-2 py-1 focus:outline-primary"
            value={data.language}
            onChange={handleOnChange}
          />
        </div>

        <div className="flex flex-col gap-1">
          <label htmlFor="profile_pic">
            Photo :
            <div className="h-14 bg-slate-200 flex justify-center items-center border rounded hover:border-primary cursor-pointer">
              <p className="text-sm max-w-[300px] text-ellipsis line-clamp-1">
                {uploadPhoto ? uploadPhoto : "Upload profile photo"}
              </p>
            </div>
          </label>

          <input
            type="file"
            id="profile_pic"
            name="profile_pic"
            className="bg-slate-100 px-2 py-1 focus:outline-primary hidden"
            onChange={handleUploadPhoto}
          />
        </div>

        <button
          type="submit"
          className="bg-slate-300 text-lg px-4 py-1 hover:bg-slate-400 rounded mt-2 font-bold leading-relaxed tracking-wide"
        >
          Register
        </button>
      </form>

      <p className="my-3 text-center">
        Already have an account?{" "}
        <Link
          href="/login"
          className="font-medium text-blue-600 dark:text-blue-500 hover:underline"
        >
          Login
        </Link>
      </p>
      {open && (
        <AlertSnackbar
          open={open}
          setOpen={setOpen}
          type={status}
          message={
            status === "success"
              ? "Registration successful!"
              : "An error occurred."
          }
        />
      )}
    </div>
  );
}
