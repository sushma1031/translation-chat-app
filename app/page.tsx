"use client";
import Link from 'next/link'
import React, { useEffect, useState } from "react";
import createAPIConfig from "./config/config.js"
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/navigation';
import { RootState } from './redux/store.ts';
import { logout, setUser } from './redux/userSlice.ts';
import io from "socket.io-client";

export default function Home() {
  const user = useSelector((state: RootState) => state?.user);
  const dispatch = useDispatch();
  const router = useRouter();

  const fetchUserDetails = async () => {
    const apiConfig = createAPIConfig();
    //To Do: get user's name here somehow
    try {
      const response = await apiConfig.get("/users/name/details", { withCredentials: true });
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
      console.log(data);
    })

    return () => {
      socketConn.disconnect();
    }
  }, [])

  return (
    <>
      <h1>Home</h1>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="z-10 w-full max-w-5xl items-center justify-center text-sm lg:flex">
          <p>Hi <span className='capitalize'>{user.name}</span>! Your preferred language of communication is: <span className="capitalize">{user.language}</span></p>
        </div>
      </main>
    </>
  );
}
