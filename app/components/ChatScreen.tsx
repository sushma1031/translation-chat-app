'use client';
import { useParams } from 'next/navigation';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { useEffect } from 'react';
import { Socket } from 'socket.io-client';
export default function ChatScreen() {
  const params = useParams();
  const socketConn: Socket | null = useSelector((state: RootState) => state?.user?.socketConnection);
  useEffect(() => {
    if (socketConn) {
      socketConn.emit("chat", params.userId);
    }
  }, [socketConn]);
  return <>
    <p>Messages!</p>
  </>
}