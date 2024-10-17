"use client";

import React, { useEffect, useState } from "react";
import createAPIConfig from "./config/config.js"
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/navigation';
import { RootState } from './redux/store.ts';
import { logout, setUser, setOnlineUsers, setSocketConnection } from './redux/userSlice.ts';
import io from "socket.io-client";

export default function UserHome() {
  const user = useSelector((state: RootState) => state?.user);
  const dispatch = useDispatch();
  const router = useRouter();

  const fetchUserDetails = async () => {
    const apiConfig = createAPIConfig();
    //To Do: get user's name here somehow
    try {
      const response = await apiConfig.get("/user-details", { withCredentials: true });
      if (response.data.logout) {
        dispatch(logout());
        router.push("/login");
      }
      dispatch(setUser(response.data.data));
    } catch (error) {
      console.log(`Error: ${error}`)
    }
  }
  useEffect(() => {
    fetchUserDetails();
  }, [])

  // socket connection
  useEffect(() => {
    const socketConn = io("http://localhost:5328", {
      withCredentials: true
    });
    socketConn.on("user_online", (data) => {
      dispatch(setOnlineUsers(data));
      console.log("Socket connected: ", socketConn.connected);
    })

    socketConn.on("disconnect", () => {
      console.log("Socket disconnected");
    });

    dispatch(setSocketConnection(socketConn));

    return () => {
      socketConn.disconnect();
    }
  }, [])

  return (
    <>
      <h1 className="text-center">User Home</h1>
      <main className="flex flex-col items-center justify-between p-24">
        <div className="z-10 w-full max-w-5xl items-center justify-center text-sm lg:flex">
          <p>Hi <span className='capitalize'>{user.name}</span>! Your preferred language of communication is: <span className="capitalize">{user.language}</span></p>
        </div>
        <div>
          Users:
          TO DO: Fetch users to select from
          {/* On selecting, do router.push(`/chat/${userId}`) */}
        </div>
      </main>
    </>
  );
}
