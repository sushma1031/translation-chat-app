"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import createAPIConfig from "../config/config.js"
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/navigation';
import { RootState } from '../redux/store.ts';
import { logout, setUser, setOnlineUsers, setSocketConnection } from '../redux/userSlice.ts';
import io from "socket.io-client";
import { Button } from "@mui/material";

interface User{
  name: string,
  language: string,
  _id: string,
  profile_pic?: string
}

export default function UserHome() {
  const user = useSelector((state: RootState) => state?.user);
  const dispatch = useDispatch();
  const router = useRouter();
  const [chatUsers, setChatUsers] = useState([] as User[])

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

  const logoutUser = async () => {
    const apiConfig = createAPIConfig();
    const response = await apiConfig.get("/logout");
    if (response.data.error) return;
    dispatch(logout());
    router.push("/login");
  };

  const fetchAvailableUsers = async () => {
    const apiConfig = createAPIConfig();
     try {
       const response = await apiConfig.get("/users", {
         withCredentials: true,
       });
       if (response.data.error) {
         console.log(`Error fetching users: ${response.data.message}`)
       }
       let users = response.data.data;
       users = users.filter((u: User, i: number) => {
         return users[i]["_id"] != user?._id
       });
       setChatUsers(users);
     } catch (error) {
       console.log(`Error: ${error}`);
     }
  }

  useEffect(() => {
    fetchUserDetails();
  }, [])

  useEffect(() => {
    fetchAvailableUsers();
  }, [user])

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
      <main className="text-center mx-auto mt-4">
        <div className="w-full items-center justify-center text-sm lg:flex">
          <p className="text-center pb-5 text-lg">
            Hi <span className="font-bold">{user.name}</span>! Your preferred
            language of communication is:{" "}
            <span className="code bg-blue-100">{user.language}</span>
          </p>
        </div>
        <div className="text-center pt-3">
          <p className="underline">Available Users</p>
          <br />
        </div>

        <div className="relative overflow-x-auto flex justify-center">
          <table className="w-6/12 text-sm text-center rtl:text-right text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-300">
              <tr>
                <th scope="col" className="px-6 py-3">
                  Name
                </th>
                <th scope="col" className="pl-6 py-3">
                  Communication Language
                </th>
              </tr>
            </thead>
            <tbody>
              {chatUsers.map((u, i) => 
                <tr className="bg-white border-b" key={i}>
                  <th
                    scope="row"
                    // className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                  >
                    <Link
                      key={i}
                      className="text-center font-medium text-blue-600 hover:underline capitalize"
                      href={`/chat/${u._id}`}
                    >
                      {`${u.name}`}
                    </Link>
                  </th>
                  <td className="px-6 py-3">{u.language}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="pt-10 text-white">
          <Button
            onClick={logoutUser}
            variant="contained"
            className="bg-blue-500"
          >
            Logout
          </Button>
        </div>
      </main>
    </>
  );
}
