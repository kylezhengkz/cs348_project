import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { useAuth } from "../../../wrappers/AuthContext";
import { useNavigate } from "react-router-dom";

export function Header() {
    const navigate = useNavigate();
    const { authUserId, setAuthUserId } = useAuth();
    
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        News
                    </Typography>
                    {authUserId !== null && <Button color="inherit">{authUserId}</Button>}
                    {authUserId !== null && <Button color="inherit" onClick={() => setAuthUserId(null)}>Logout</Button>}
                    {authUserId === null && <Button color="inherit" onClick={() => navigate("/login")}>Login</Button>}
                </Toolbar>
            </AppBar>
        </Box>
    );
}