import { createSlice } from "@reduxjs/toolkit";
import { Socket } from "socket.io-client";

const initialState = {
  _id : "",
  name : "",
  email : "",
  profile_pic: "",
  language: "",
  token : "",
  onlineUsers : [],
  socketConnection : null as Socket | null
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action) => {
        state._id = action.payload._id
        state.name = action.payload.name 
        state.email = action.payload.email
        state.language = action.payload.language
        state.profile_pic = action.payload.profile_pic 
    },
    setToken: (state, action) => {
        state.token = action.payload
    },
    logout: (state) => {
        state._id = ""
        state.name = ""
        state.email = ""
        state.profile_pic = ""
        state.language = ""
        state.token = ""
        state.socketConnection = null
    },
    setOnlineUsers: (state, action)=>{
      state.onlineUsers = action.payload
    },
    setSocketConnection: (state, action)=>{
      state.socketConnection = action.payload
    }
  },
})

export const { setUser, setToken, logout, setOnlineUsers, setSocketConnection } = userSlice.actions

export default userSlice.reducer

