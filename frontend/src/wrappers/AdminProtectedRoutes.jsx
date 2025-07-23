import { USER_PERMS } from "../constants/authContants";
import { useAuth } from "./AuthContext";
import { Navigate } from "react-router-dom";

export function AdminProtectedRoutes({children}) {
  const { userPerm, loading } = useAuth();
  
  if (loading) return <div>Loading...</div>;
  
  if (userPerm !== USER_PERMS.ADMIN) {
    return <Navigate to="/accessDenied" replace />;
  }

  return children;
}
