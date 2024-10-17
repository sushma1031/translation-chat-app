"use client";
import { useParams } from "next/navigation";
import { useSelector } from "react-redux";
import { RootState } from "../../redux/store";
import { useEffect } from "react";
import { Socket } from "socket.io-client";

//ren: 670f8169493e3e689b4715e4

export default function ChatScreen() {
  const params = useParams();
  const socketConn: Socket | null = useSelector(
    (state: RootState) => state?.user?.socketConnection
  );
  useEffect(() => {
    if (socketConn) {
      if (!socketConn.connected) {
        console.log("Socket not connected, attempting to reconnect...");
        socketConn.connect();
      }
      socketConn.emit("chat", params.userId);

      socketConn.on("user_status", (data) => {
        console.log("user status:", data);
      });
    }
  }, [socketConn, params.userId]);
  return (
    <>
      <p>Messages!</p>
    </>
  );
}
