import { useEffect } from "react";
import { useLocation } from "react-router-dom";

export function RouteTracker() {
    const location = useLocation();

    useEffect(() => {
        const excludedPaths = ["/login", "/signup", "/splash", "/accessDenied"];
        if (!excludedPaths.includes(location.pathname)) {
            sessionStorage.setItem("lastVisitedPath", location.pathname);
        }
    }, [location]);

    return null;
}