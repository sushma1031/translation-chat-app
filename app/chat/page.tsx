"use client";
import { FormEvent, useState } from "react";
import axios from "axios";

export default function Chat() {
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  
  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    try {
      const response = await axios({
        method: "post",
        url: "http://localhost:5328/api/translate/image",
        data: {
          text: inputText,
        },
      });

      setTranslatedText(response.data.translated);
    } catch (error) {
      console.error("Error translating text: ", error);
    }
  }

  return (
    <>
      <h1>Chat Room</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="userText">Enter text: </label>
        <input
          name="userText"
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <br />
        <button type="submit">Translate</button>
      </form>
      {translatedText && <p>Result: {translatedText}</p>}
    </>
  );
}