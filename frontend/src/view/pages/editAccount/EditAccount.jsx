import { Container, Box, Typography, FormControl, Paper, Stack } from "@mui/material"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useState, useRef } from "react";

import { userService } from "../../../model/UserService";
import { PopupInfo } from "../../components/popupInfo/PopupInfo";
import { useAuth } from "../../../wrappers/AuthContext";


export function EditAccount() {
    const { authUserId, setUsername } = useAuth();

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
        const [success, message] = await userService.updateUsername(authUserId, newUsername);

        if (success) {
            setUsername(newUsername);
        }

        showAlert(success, message);
    };

    const handlePasswordUpdate = async () => {
        const newPassword = newPasswordRef.current.value;
        const oldPassword = oldPasswordRef.current.value;
        const [ success, message ] = await userService.updatePassword(authUserId, oldPassword, newPassword);
        showAlert(success, message);
    };
    
    return (
        <Container>
            <Box sx={{ minHeight: "80vh", py: 5 }}>
                <Typography variant="h3" align="center" gutterBottom>
                    Edit Account
                </Typography>

                <Stack spacing={5} alignItems="center">
                    {/* Username Box */}
                    <Paper elevation={2} sx={{ p: 4, width: '100%', maxWidth: 500, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6" gutterBottom>
                            Update Username
                        </Typography>
                        <Stack spacing={2}>
                            <TextField
                                label="New Username"
                                variant="outlined"
                                inputRef={newUsernameRef}
                                fullWidth
                                InputProps={{
                                    sx: {
                                        '& input:-webkit-autofill': {
                                        boxShadow: '0 0 0 1000px #f5f5f5 inset',
                                        WebkitTextFillColor: '#000',
                                        },
                                    }
                                }}
                            />
                            <Button
                                variant="contained"
                                sx={{ backgroundColor: '#9b5fa0' }}
                                onClick={handleUsernameUpdate}
                            >
                                Update Username
                            </Button>
                        </Stack>
                    </Paper>

                    {/* Password Box */}
                    <Paper elevation={2} sx={{ p: 4, width: '100%', maxWidth: 500, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6" gutterBottom>
                            Update Password
                        </Typography>
                        <Stack spacing={2}>
                            <TextField
                                label="Old Password"
                                type="password"
                                variant="outlined"
                                inputRef={oldPasswordRef}
                                fullWidth
                                InputProps={{
                                    sx: {
                                        '& input:-webkit-autofill': {
                                        boxShadow: '0 0 0 1000px #f5f5f5 inset',
                                        WebkitTextFillColor: '#000',
                                        },
                                    }
                                }}
                            />
                            <TextField
                                label="New Password"
                                type="password"
                                variant="outlined"
                                inputRef={newPasswordRef}
                                fullWidth
                            />
                            <Button
                                variant="contained"
                                sx={{ backgroundColor: '#9b5fa0' }}
                                onClick={handlePasswordUpdate}
                            >
                                Update Password
                            </Button>
                        </Stack>
                    </Paper>
                </Stack>

                <PopupInfo
                    open={alertOpen}
                    onClose={() => setAlertOpen(false)}
                    alertSeverity={alertSeverity}
                >
                    {alertMessage}
                </PopupInfo>
            </Box>
        </Container>
    );
}