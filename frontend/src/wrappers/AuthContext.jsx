import { useState, createContext, useContext, useEffect } from "react"

const AuthContext = createContext()

export function AuthProvider({children}) {
  const [authUserId, setAuthUserId] = useState(() => sessionStorage.getItem("authUserId"));

  useEffect(() => {
    if (authUserId !== null) {
      sessionStorage.setItem("authUserId", authUserId);
    }
  }, [authUserId]);

  return (
    <AuthContext.Provider value={{authUserId, setAuthUserId}}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
