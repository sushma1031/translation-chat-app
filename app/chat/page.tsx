"use client";
import { FormEvent, useState, useRef } from "react";
import { createAPIConfig } from "../config/config.js";

const apiConfig = createAPIConfig();

export default function Chat() {
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  async function handleImageSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fileInput = fileInputRef.current;

    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
      alert("Please upload a file");
      return;
    }
    const formData = new FormData();

    formData.append("src", "kannada");
    formData.append("dest", "english");
    let response = {
      data: {
        translated: "",
      },
    };
    try {
      formData.append("file", fileInput.files[0]);
      response = await apiConfig.post("translate/image", formData);

      setTranslatedText(response.data.translated);
    } catch (error) {
      console.error("Error translating text: ", error);
    }
  }
  
  async function handleAudioSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData();
    let src = "hindi";
    e.preventDefault();
    const fileInput = fileInputRef.current;

    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
      alert("Please upload a file");
      return;
    }
    formData.append("src", src);
    formData.append("dest", "english");
    let response = {
      data: {
        translated: "",
      },
    };
    try {
      formData.append("file", fileInput.files[0]);
      response = await apiConfig.post("translate/audio", formData);

      setTranslatedText(response.data.translated);
    } catch (error) {
      console.error("Error translating text: ", error);
    }
  }

  async function handleVideoSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData();
    const response = await apiConfig.post("translate/subtitles", { src: "hindi", dest: "english" });
    setTranslatedText(response.data.data);
  }

  return (
    <>
      <h1>Chat Room</h1>
      <form onSubmit={handleAudioSubmit}>
        <label htmlFor="userText">Enter text: </label>
        <input
          name="userText"
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <br />
        <br />
        <input
          type="file"
          name="file"
          id="file"
          accept="image/png, image/jpeg"
          ref={fileInputRef}
        />
        <br />
        <br />
        <input
          type="file"
          name="file"
          id="file"
          accept="audio/wav"
          ref={fileInputRef}
        />
        <br />
        <br />
        <button type="submit">Translate</button>
      </form>
      {translatedText && <p>Result: {translatedText}</p>}
    </>
  );
}
