import { useState, createContext, useContext, useEffect } from "react"

const AuthContext = createContext()

export function AuthProvider({children}) {
  const [authUserId, setAuthUserId] = useState(() => sessionStorage.getItem("authUserId"));
  const [username, setUsername] = useState(() => sessionStorage.getItem("username"));
  const [userPerm, setUserPerm] = useState(() => {
    const perm = sessionStorage.getItem("userPerm");
    return perm != null ? Number(perm) : null;
  });

  useEffect(() => {
    if (authUserId !== null) {
      sessionStorage.setItem("authUserId", authUserId);
    } else {
      sessionStorage.removeItem("authUserId");
    }
  }, [authUserId]);

  useEffect(() => {
    if (username !== null) {
      sessionStorage.setItem("username", username);
    } else {
      sessionStorage.removeItem("username");
    }
  }, [username]);

  useEffect(() => {
    if (userPerm !== null) {
      sessionStorage.setItem("userPerm", String(userPerm));
    } else {
      sessionStorage.removeItem("userPerm");
    }
  }, [userPerm]);

  const logout = () => {
    setAuthUserId(null);
    setUsername(null);
    setUserPerm(null);
  };

  return (
    <AuthContext.Provider value={{authUserId, setAuthUserId, username, setUsername, userPerm, setUserPerm, logout}}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
