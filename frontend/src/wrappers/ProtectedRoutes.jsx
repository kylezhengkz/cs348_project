import { useAuth } from "./AuthContext"
import { Navigate } from "react-router-dom";

export function ProtectedRoutes({children}) {
  const { authUserId } = useAuth()

  console.log("SEE HERE", authUserId)
  
  return (
    authUserId === null ? <Navigate to="/login"/> : children
  )
}
