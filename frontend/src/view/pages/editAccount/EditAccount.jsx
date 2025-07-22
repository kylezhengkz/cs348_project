import { Container, Box, Typography } from "@mui/material"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useState } from "react";


export function EditAccount() {
    const [oldUsername, setOldUsername] = useState("");
    const [newUsername, setNewUsername] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");

    const handleUsernameUpdate = async () => {
        try {
            const res = await dashBoardService.updateUsername(oldUsername, newUsername);
            if (res.success) {
                setAlertSeverity("success");
                setAlertMessage("Username updated successfully!");
            } else {
                setAlertSeverity("error");
                setAlertMessage(res.message || "Failed to update username.");
            }
        } catch (err) {
            console.error(err);
            setAlertSeverity("error");
            setAlertMessage("Server error occurred.");
        } finally {
            setAlertOpen(true);
        }
    };

    const handlePasswordUpdate = async () => {
        try {
            const res = await dashBoardService.updatePassword(authUserId, oldPassword, newPassword);
            if (res.success) {
                setAlertSeverity("success");
                setAlertMessage("Password updated successfully!");
            } else {
                setAlertSeverity("error");
                setAlertMessage(res.message || "Failed to update password.");
            }
        } catch (err) {
            console.error(err);
            setAlertSeverity("error");
            setAlertMessage("Server error occurred.");
        } finally {
            setAlertOpen(true);
        }
    };

    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h2" gutterBottom>Edit Account</Typography>

                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Update Username</Typography>
                        <TextField
                            fullWidth
                            label="Old Username"
                            margin="normal"
                            value={oldUsername}
                            onChange={(e) => setOldUsername(e.target.value)}
                        />
                        <TextField
                            fullWidth
                            label="New Username"
                            margin="normal"
                            value={newUsername}
                            onChange={(e) => setNewUsername(e.target.value)}
                        />
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleUsernameUpdate}
                            sx={{ mt: 2 }}
                        >
                            Update Username
                        </Button>
                        <Typography variant="body1" className="mt-2">
                            
                        </Typography>
                    </Box>

                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Update Password</Typography>
                        <Typography variant="body1" className="mt-2">
                            <TextField
                                fullWidth
                                type="password"
                                label="Old Password"
                                margin="normal"
                                value={oldPassword}
                                onChange={(e) => setOldPassword(e.target.value)}
                            />
                            <TextField
                                fullWidth
                                type="password"
                                label="New Password"
                                margin="normal"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                            />
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handlePasswordUpdate}
                                sx={{ mt: 2 }}
                            >
                                Update Password
                            </Button>
                        </Typography>
                    </Box>
                </Box>
            </Box>
        </Container>
    );
}