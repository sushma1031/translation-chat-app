"use client";
import { FormEvent, useState } from "react";
import { createAPIConfig } from "../config/config.js";
import * as Echogarden from "echogarden";

const apiConfig = createAPIConfig();

export default function Chat() {
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");

  async function handleAudioSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData();
    let src = "hindi";
    let files = (e.target as HTMLInputElement).files;
    if (!files || files.length == 0) {
      alert("Please upload an audio file");
      return;
    }

    let file = files[0];

    formData.append("src", src);
    formData.append("dest", "english");
    let response = {
      data: {
        translated: "",
      },
    };
    try {
      if (src == "english") {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const arrayBuffer = (e.target && e.target.result) as ArrayBuffer;
          const uint8Array = new Uint8Array(arrayBuffer);
          const transcribed = await Echogarden.recognize(uint8Array, {
            language: "en",
            whisper: { model: "tiny.en" },
          });
          formData.append("transcribed", transcribed.transcript); // send the transcribed text itself
          // should we have a different endpoint?
          response = await apiConfig.post("translate/audio", formData);
        };
        reader.readAsArrayBuffer(file);
      } else {
        formData.append("file", "file");
        response = await apiConfig.post("translate/audio", formData);
      }

      setTranslatedText(response.data.translated);
    } catch (error) {
      console.error("Error translating text: ", error);
    }
  }

  async function handleVideoSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData();
    
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
        <input type="file" name="audioFile" id="audioFile" />
        <br />
        <button type="submit">Translate</button>
      </form>
      {translatedText && <p>Result: {translatedText}</p>}
    </>
  );
}
