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
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";
import uploadToCloud from "./util";

interface UploadedMedia {
  isUploaded: boolean;
  mediaRef: React.MutableRefObject<HTMLInputElement | null>;
  type: "image" | "audio" | "video" | "";
}

export default function ChatScreen() {
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
  useEffect(() => {
    if (socketConn) {
      if (!socketConn.connected) {
        console.log("Socket not connected, attempting to reconnect...");
        socketConn.connect();
      }
      socketConn.emit("chat", params.userId);

      socketConn.on("user_status", (data) => {
        console.log("user status fetched");
        setChatUser(data);
      });
    }
  }, [socketConn, params.userId, user]);

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
      setLoading(true);
      const url = await uploadToCloud(file, type);
      setLoading(false);
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

    if (message.text || message.audioUrl || message.imageUrl || message.videoUrl) {
      if (socketConn) {
        socketConn.emit("new_message", {
          sender: user?._id,
          receiver: params.userId,
          text: message.text,
          imageUrl: message.imageUrl,
          videoUrl: message.videoUrl,
          src_lang: user.language,
          dest_lang: chatUser.language,
        });
        setMessage({
          text: "",
          imageUrl: "",
          videoUrl: "",
          audioUrl: ""
        });
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
                  <p>
                    Media: {uploadedMedia.mediaRef.current?.files[0].name}
                  </p>
                </div>
              </div>
            )}
        </div>
      </section>
      <section id="sendBar" className="h-16 bg-white flex items-center">
        <div className="relative">
          <div className="ps-3 flex justify-center items-center">
            {/* <IconButton
              aria-label="attach media"
              onClick={() => {
                setToggleMediaUpload((prev) => !prev);
              }}
            >
              <AddIcon />
            </IconButton> */}
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

          {/* upload media */}
          {}
        </div>
        <form className="h-full w-full flex gap-2 pe-5" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Your message"
            className="py-1 px-4 outline-none w-full h-full"
            value={message.text}
            onChange={handleTextChange}
          />
          <button type="submit">Send</button>
        </form>
      </section>
    </>
  );
}