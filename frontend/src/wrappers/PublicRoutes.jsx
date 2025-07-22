import { Navigate } from "react-router-dom";
import { useAuth } from "../wrappers/AuthContext";

export function PublicRoutes({ children }) {
    const { authUserId } = useAuth();

    if (authUserId) {
        return <Navigate to="/home" replace />;
    }

    return children;
}