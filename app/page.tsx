"use client";
import Link from "next/link";
import { Button } from "@mui/material";

export default function Home() {
  return (
    <>
      <main className="mx-auto">
        <div className="w-full flex flex-row justify-between items-center">
          <div className="ps-16 flex flex-col h-[85vh] justify-center gap-2">
            <h1 className="text-3xl text-center font-bold">Welcome to Bridge!</h1>
            <p className="text-center">
              Empowering global communication, bridging cultures, and building a
              world without language limits
            </p>
            <Button
              variant="contained"
              className="self-center contained-button mt-8"
            >
              <Link
                href={"/register"}
                className="text-center font-medium"
              >
                <p className="capitalize">Get Started</p>
              </Link>
            </Button>
          </div>
          <div className="">
            <img src="/hero.png" alt="" />
          </div>
        </div>
      </main>
    </>
  );
}
