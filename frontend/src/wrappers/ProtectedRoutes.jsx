import { useAuth } from "./AuthContext"
import { Navigate } from "react-router-dom";

export function ProtectedRoutes({children}) {
  const { authUserId } = useAuth()
  
  return (
    authUserId === null ? <Navigate to="/"/> : children
  )
}
