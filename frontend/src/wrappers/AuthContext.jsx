import { useState, createContext, useContext, useEffect } from "react"

const AuthContext = createContext()

export function AuthProvider({children}) {
  const [authUserId, setAuthUserId] = useState(() => sessionStorage.getItem("authUserId"));
  const [username, setUsername] = useState(() => sessionStorage.getItem("username"));
  const [userPerm, setUserPerm] = useState(() => sessionStorage.getItem("userPerm"));

  useEffect(() => {
    if (authUserId !== null) {
      sessionStorage.setItem("authUserId", authUserId);
    }
  }, [authUserId]);

  useEffect(() => {
    if (username !== null) {
      sessionStorage.setItem("username", username);
    }
  }, [username]);

  useEffect(() => {
    if (userPerm !== null) {
      sessionStorage.setItem("userPerm", userPerm);
    }
  }, [userPerm]);

  return (
    <AuthContext.Provider value={{authUserId, setAuthUserId, username, setUsername, userPerm, setUserPerm}}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
