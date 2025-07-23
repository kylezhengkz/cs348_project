import { Container, Box, Typography, FormControl } from "@mui/material"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useState, useRef } from "react";

import { userService } from "../../../model/UserService";
import { PopupInfo } from "../../components/popupInfo/PopupInfo";
import { useAuth } from "../../../wrappers/AuthContext";


export function EditAccount() {
    const { authUserId } = useAuth();

    const newUsernameRef = useRef();
    const oldPasswordRef = useRef();
    const newPasswordRef = useRef();

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    function showAlert(success, message) {
        const alertType = success ? "success" : "error";
        setAlertSeverity(alertType);
        setAlertMessage(message);
        setAlertOpen(true);
    }

    const handleUsernameUpdate = async () => {
        const newUsername = newUsernameRef.current.value;

        console.log("YSER ID: ", authUserId);

        const [success, message] = await userService.updateUsername(authUserId, newUsername);
        showAlert(success, message);
    };

    const handlePasswordUpdate = async () => {
        const newPassword = newPasswordRef.current.value;
    
        const { success, message } = await userService.updatePassword(authUserId, newPassword);
        showAlert(success, message);
    };
    
    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h2" gutterBottom>Edit Account</Typography>
                </Box>
                
                <Box justifyContent="center" display="flex" className="mt-5">
                    <FormControl sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Update Username</Typography>
                        <TextField
                            fullWidth
                            label="New Username"
                            margin="normal"
                            variant="outlined"
                            inputRef={newUsernameRef}
                        />
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleUsernameUpdate}
                            sx={{ mt: 2 }}
                        >
                            Update Username
                        </Button>
                        <Typography variant="body1" className="mt-2"></Typography>
                    </FormControl>
                </Box>
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Update Password</Typography>
                        <FormControl variant="body1" className="mt-2">
                            <TextField
                                fullWidth
                                type="password"
                                label="Old Password"
                                margin="normal"
                                variant="outlined"
                                inputRef={oldPasswordRef}
                            />
                            <TextField
                                fullWidth
                                type="password"
                                label="New Password"
                                margin="normal"
                                variant="outlined"
                                inputRef={newPasswordRef}
                            />
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handlePasswordUpdate}
                                sx={{ mt: 2 }}
                            >
                                Update Password
                            </Button>
                        </FormControl>
                    </Box>
                </Box>
            </Box>

            <PopupInfo open={alertOpen} onClose={() => setAlertOpen(false)} alertSeverity={alertSeverity}>
                {alertMessage}
            </PopupInfo>
        </Container>
    );
}