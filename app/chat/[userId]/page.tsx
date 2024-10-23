"use client";
import { useParams } from "next/navigation";
import { useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { useEffect, useState, useRef, FormEvent } from "react";
import { Socket } from "socket.io-client";
import ImageIcon from "@mui/icons-material/Image";
import VideocamIcon from "@mui/icons-material/Videocam";
import AudioFileIcon from "@mui/icons-material/AudioFile";
import CloseIcon from "@mui/icons-material/Close";
import SendIcon from "@mui/icons-material/Send";
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";
import uploadToCloud from "./util";

interface UploadedMedia {
  isUploaded: boolean;
  mediaRef: React.MutableRefObject<HTMLInputElement | null>;
  type: "image" | "audio" | "video" | "";
}

interface Message {
  original_lang?: string;
  text?: string;
  trans_text?: string; 
  image_url?: string; 
  video_url?: string; 
  trans_video_url?: string; 
  audio_url?: string; 
  trans_audio_url?: string; 
  seen?: boolean; 
  sent_by: string;
  sent_at: string;
}

const testMessage: Message = {
  text: "apple",
  trans_text: "सेब",
  sent_by: "67126b669cbba43ac05f80e4",
  sent_at: "2024-10-20T17:09:17.884000",
  // video_url:
  //   "https://res.cloudinary.com/dznw8d1fj/video/upload/v1729324865/trans-chat/audio/hindi-1_cu4wcl.mp4",
  // trans_video_url:
  //   "https://res.cloudinary.com/dznw8d1fj/video/upload/v1729324865/trans-chat/audio/hindi-1_cu4wcl.mp4",
  audio_url:
    "https://res.cloudinary.com/dznw8d1fj/video/upload/v1729325550/trans-chat/audio/a-hindi-1-translated.mp3",
  trans_audio_url:
    "https://res.cloudinary.com/dznw8d1fj/video/upload/v1729325550/trans-chat/audio/a-hindi-1-translated.mp3",
};

export default function ChatScreen() {
  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    });
  };

  const params = useParams();
  const socketConn: Socket | null = useSelector(
    (state: RootState) => state?.user?.socketConnection
  );
  const user = useSelector((state: RootState) => state?.user);
  const [chatUser, setChatUser] = useState({
    name: "",
    email: "",
    profile_pic: "",
    language: "",
    online: false,
    _id: "",
  });

  const audioInputRef = useRef<HTMLInputElement | null>(null);
  const imageInputRef = useRef<HTMLInputElement | null>(null);
  const videoInputRef = useRef<HTMLInputElement | null>(null);
  const [uploadedMedia, setUploadedMedia] = useState({
    isUploaded: false,
    mediaRef: {
      current: null,
    } as React.MutableRefObject<HTMLInputElement | null>,
    type: ""
  } as UploadedMedia);
  const [message, setMessage] = useState({
    text: "",
    imageUrl: "",
    audioUrl: "",
    videoUrl: "",
  });
  const [loading, setLoading] = useState(false);
  const [chatMsgs, setChatMsgs] = useState([] as Message[]);
  const currentMessage = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    console.log(chatMsgs);
    if (currentMessage.current) {
      currentMessage.current.scrollIntoView({
        behavior: "smooth",
        block: "end",
      });
    }
  }, [chatMsgs]);
  useEffect(() => {
    if (socketConn) {
      if (!socketConn.connected) {
        console.log("Socket not connected, attempting to reconnect...");
        socketConn.connect();
      }
      socketConn.emit("chat", user?._id, params.userId);

      socketConn.on("user_status", (data) => {
        console.log("Chat receiver data fetched");
        setChatUser(data);
      });

      socketConn.on("message", (data) => {
        console.log("Message data:", data);
        setLoading(false);
        if(data)
          setChatMsgs(data);
      });
    }
  }, [socketConn, params.userId, user]);

  const clearUpload = (type: "image" | "audio" | "video") => {
    switch (type) {
      case "image": if (imageInputRef.current) imageInputRef.current.value = '';
      case "audio": if (audioInputRef.current) audioInputRef.current.value = '';
      case "video": if (videoInputRef.current) videoInputRef.current.value = '';
    }
    setUploadedMedia((prev) => ({ ...prev, isUploaded: false, type: "" }));
  }

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage((prev) => ({...prev, text: e.target.value}));
  }

  const handleSendMessage = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const audioFile = audioInputRef.current;
    const imageFile = imageInputRef.current;
    const videoFile = videoInputRef.current;

    const uploadFileIfExists = async (fileInput: HTMLInputElement | null, type: "image" | "video") => {
      if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        return "";
      }
      let file = fileInput.files[0];
      setUploadedMedia((p) => ({ ...p, isUploaded: false }));
      setLoading(true);
      const url = await uploadToCloud(file, type);
      return url;
    };

    let audioUrl = await uploadFileIfExists(audioFile, "video");
    let videoUrl = await uploadFileIfExists(videoFile, "video");
    let imageUrl = await uploadFileIfExists(imageFile, "image");

    setMessage((prev) => {
      return {
        ...prev,
        audioUrl,
        videoUrl,
        imageUrl
      }
    });

    if (message.text || audioUrl || imageUrl || videoUrl) {
      if (socketConn) {
        socketConn.emit("new_message", {
          sender: user?._id,
          receiver: params.userId,
          text: message.text,
          imageUrl: imageUrl,
          audioUrl: audioUrl,
          videoUrl: videoUrl,
          src_lang: user.language,
          dest_lang: chatUser.language,
        });
        console.log("Sent successfully!");
        setLoading(false);
        setMessage({
          text: "",
          imageUrl: "",
          videoUrl: "",
          audioUrl: ""
        });
        clearUpload("image");
        clearUpload("audio");
        clearUpload("video");
      }
    }
  };
  return (
    <>
      <p className="pb-2">
        Messages with {chatUser.name}!{" "}
        {`(Currently ${chatUser.online ? "online" : "offline"})`}
      </p>
      <section
        id="messages"
        className="h-[calc(100vh-128px)] bg-blue-200 overflow-x-hidden overflow-y-scroll"
      >
        <div>
          <div className="flex flex-col gap-2 py-2 mx-2" ref={currentMessage}>
            {Boolean(chatMsgs) && chatMsgs.map((msg, index) => {
              return (
                <div
                  key={index}
                  className={`p-1 py-1 rounded w-fit max-w-[280px] md:max-w-sm lg:max-w-md ${
                    user._id === msg?.sent_by
                      ? "ml-auto bg-teal-100"
                      : "bg-white"
                  }
                    }`}
                >
                  <div className="w-full relative">
                    {msg?.image_url && (
                      <img
                        src={msg?.image_url}
                        className="w-full h-full object-scale-down"
                      />
                    )}
                    {msg?.video_url && (
                      <video
                        src={
                          user._id === msg?.sent_by
                            ? msg.video_url
                            : msg.trans_video_url
                        }
                        className="w-full h-full object-scale-down"
                        controls
                      />
                    )}
                    {msg?.audio_url && (
                      <audio
                        src={
                          user._id === msg?.sent_by
                            ? msg.audio_url
                            : msg.trans_audio_url
                        }
                        className="bg-transparent"
                        controls
                      />
                    )}
                  </div>
                  <p className="px-2">
                    {user._id === msg?.sent_by ? msg.text : msg.trans_text}
                  </p>
                  <p className="text-xs ml-auto w-fit">
                    {formatTime(msg.sent_at)}
                  </p>
                </div>
              );
            })}
          </div>
          {/**display uploaded media*/}
          {uploadedMedia.isUploaded &&
            uploadedMedia.mediaRef.current?.files && (
              <div className="w-full h-[calc(100vh-128px)] sticky bottom-0 bg-slate-700 bg-opacity-30 flex justify-center items-center rounded overflow-hidden">
                <div className="w-fit p-2 absolute top-0 right-0 cursor-pointer">
                  <IconButton
                    onClick={() => {
                      if (uploadedMedia.type) clearUpload(uploadedMedia.type);
                    }}
                    className="hover:text-red-600"
                  >
                    <CloseIcon />
                  </IconButton>
                </div>
                <div className="bg-white p-3">
                  {/* <img
                    // src={imageInputRef.current}
                    className="aspect-square w-full h-full max-w-sm m-2 object-scale-down"
                  /> */}
                  <p>Media: {uploadedMedia.mediaRef.current?.files[0].name}</p>
                </div>
              </div>
            )}
        </div>
        {loading && (
          <div className="w-full h-full flex sticky bottom-0 justify-center items-center">
            <p>Loading...</p>
          </div>
        )}
      </section>
      <section id="sendBar" className="h-16 bg-white flex items-center">
        <div className="relative">
          <div className="ps-3 flex justify-center items-center">
            {/* upload media */}
            <form className="flex gap-2">
              <Tooltip title="Audio">
                <label
                  htmlFor="uploadAudio"
                  className="p-2 rounded-full hover:bg-slate-200 cursor-pointer"
                >
                  <div className="text-primary">
                    <AudioFileIcon />
                  </div>
                </label>
              </Tooltip>
              <Tooltip title="Image">
                <label
                  htmlFor="uploadImage"
                  className="p-2 rounded-full hover:bg-slate-200 cursor-pointer"
                >
                  <div className="text-primary">
                    <ImageIcon />
                  </div>
                </label>
              </Tooltip>
              <Tooltip title="Video">
                <label
                  htmlFor="uploadVideo"
                  className="p-2 rounded-full hover:bg-slate-200 cursor-pointer"
                >
                  <div className="text-primary">
                    <VideocamIcon />
                  </div>
                </label>
              </Tooltip>

              <input
                type="file"
                id="uploadAudio"
                accept="audio/wav"
                ref={audioInputRef}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  setUploadedMedia({
                    isUploaded: true,
                    mediaRef: audioInputRef,
                    type: "audio",
                  });
                }}
                className="hidden"
              />
              <input
                type="file"
                id="uploadImage"
                accept="image/png, image/jpeg"
                ref={imageInputRef}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  setUploadedMedia({
                    isUploaded: true,
                    mediaRef: imageInputRef,
                    type: "image",
                  });
                }}
                className="hidden"
              />

              <input
                type="file"
                id="uploadVideo"
                accept="video/mp4"
                ref={videoInputRef}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  setUploadedMedia({
                    isUploaded: true,
                    mediaRef: videoInputRef,
                    type: "video",
                  });
                }}
                className="hidden"
              />
            </form>
          </div>
        </div>
        <form
          className="h-full w-full flex gap-2 pe-5"
          onSubmit={handleSendMessage}
        >
          <input
            type="text"
            placeholder="Your message"
            className="py-1 px-4 outline-none w-full h-full"
            value={message.text}
            onChange={handleTextChange}
          />
          <button type="submit" className="hover:text-blue-700">
            <SendIcon />
          </button>
        </form>
      </section>
    </>
  );
}