import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from "react-router-dom";
import { useRef, useState } from 'react';
import Button from '@mui/material/Button';
import { USER_ROLES } from '../../../constants/authContants';

import { useAuth } from "../../../wrappers/AuthContext";
import { AccountMenu } from '../accountMenu/AccountMenu';
import "./Header.css"

export function Header() {
    const navigate = useNavigate();
    const { authUserId, setAuthUserId, username, setUsername, userPerm, setUserPerm, logout } = useAuth();

    const [showProfile, setShowProfile] = useState(false);
    const [showNavBar, setShowNavBar] = useState(false);

    const isLogin = authUserId !== null;

    const style = {
      position: 'absolute',
      top: '10%',
      left: '85%',
      transform: 'translate(-50%, -50%)',
      width: '25%',
      bgcolor: 'background.paper',
      border: '2px solid #000',
      boxShadow: 24,
      p: 4,
    };
    const profileIconRef = useRef(null);

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
                        onClick = { () => {
                            setShowNavBar(!showNavBar)
                          }
                        }
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: "bold" }}>
                        Room Booking App
                    </Typography>
                    {authUserId !== null && (
                      <>
                        <Button color="inherit" onClick={() => {
                          logout();
                        }}>Logout</Button>
                      </>
                    )}

                    {authUserId === null && <Button color="inherit" onClick={() => navigate("/login")}>Login</Button>}
                    {authUserId === null && <Button color="inherit" onClick={() => navigate("/signup")}>Signup</Button>}

                    <Button sx={{display: isLogin ? "inherit": "none"}} id="profilePic" ref={profileIconRef} onClick={() => { setShowProfile(true) }}>
                      <img src={require('../../../resources/profile.png')}></img>
                    </Button>

                    <AccountMenu 
                      username={username} 
                      anchorEl={profileIconRef} 
                      open={showProfile} 
                      onClose={() => setShowProfile(false) } 
                      logOutHandler={() => {
                        setAuthUserId(null)
                        setUsername(null)
                        setUserPerm(null)
                      }}>
                    </AccountMenu>
                </Toolbar>
            </AppBar>
        </Box>
    );
}