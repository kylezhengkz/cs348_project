import { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../../wrappers/AuthContext';

import computerSaysNo from '../../../resources/computer_says_no.jpeg';
import 'bootstrap/dist/css/bootstrap.min.css';
import './AccessDenied.css';


export function AccessDenied() {
    const timeoutSeconds = 5;
    const navigate = useNavigate();
    const { authUserId } = useAuth();
    const [countDown, setCountDown] = useState(timeoutSeconds);

    useEffect(() => {
        if (countDown <= 0) {
            const lastVisited = sessionStorage.getItem("lastVisitedPath");
            const redirectTo = authUserId
                ? lastVisited || "/home"
                : "/splash";
            navigate(redirectTo);
            return;
        }

        const timer = setTimeout(() => {
            setCountDown((prev) => prev - 1);
        }, 1000);

        return () => clearTimeout(timer);
    }, [countDown, navigate]);

    return (
        <div className="access-denied-container">
            <img src={computerSaysNo} alt="Computer says no!" className="access-denied-image" />
            <p className="access-denied-text">
                Access denied. Redirecting in {countDown} second{countDown !== 1 ? "s" : ""}...
            </p>
        </div>
    );
}
