"use client";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import createAPIConfig from "./config/config.js"
import { useRouter } from 'next/navigation';
import io from "socket.io-client";
import { Button } from "@mui/material";

interface User{
  name: string,
  language: string,
  _id: string,
  profile_pic?: string
}

export default function UserHome() {
  return(
    <>
      <h1 className="text-center py-3 text-xl">Home</h1>
      <main className="text-center mx-auto">
        <div className="w-full flex flex-col items-center justify-center">
          <h1 className="text-center text-2xl">Welcome to Bridge!</h1>
          <p className="text-center">
            Empowering global communication, bridging cultures, and building a
            world without language limits!
          </p>
          <Link
            href={"/register"}
            className="text-center font-medium text-blue-600 hover:underline capitalize"
          >
            Get Started
          </Link>
        </div>
      </main>
    </>
  );
}
