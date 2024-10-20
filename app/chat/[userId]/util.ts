// upload to cloudinary folder 'original' for video and audio, 'image' for image
// upload only once before submitting the form
import axios, { AxiosError } from 'axios';

const uploadToCloud = async (file: File, type: "image" | "video") => {
  const URL = `https://api.cloudinary.com/v1_1/${process.env.CLOUD_NAME}/${type}/upload`;
  const directory = "trans-chat";
  const formData = new FormData();
  formData.append("file", file);
  formData.append("api_key", `${process.env.API_KEY}`);
  formData.append("folder", `${directory}/${type === "image" ? "image" : "sent"}`);
  formData.append("upload_preset", "trans-chat-storage");
  
  try {
    const response = await axios.post(URL, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    // const responseData = await response.json();
    console.log("Upload successful");
    // return responseData["secure_url"];
    return response.data["secure_url"];
  } catch (error: any) {
    console.log(error.message);
    return "";
  }
  
}

export default uploadToCloud;