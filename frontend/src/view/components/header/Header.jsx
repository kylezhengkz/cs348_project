import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { useAuth } from "../../../wrappers/AuthContext";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
import Modal from '@mui/material/Modal';
import Button from '@mui/material/Button';

import "./Header.css"

export function Header() {
    const navigate = useNavigate();
    const { authUserId, setAuthUserId, username, setUsername, userPerm, setUserPerm } = useAuth();

    const [show, setShow] = useState(false);

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

    const roles = {1: "User", 2: "Admin", 3: "Manager"}

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
                    {authUserId !== null && (
                      <>
                        <Button color="inherit" onClick={() => {
                          setAuthUserId(null)
                          setUsername(null)
                          setUserPerm(null)
                        }}>Logout</Button>
                      </>
                    )}

                    {authUserId === null && <Button color="inherit" onClick={() => navigate("/login")}>Login</Button>}
                    {authUserId === null && <Button color="inherit" onClick={() => navigate("/signup")}>Signup</Button>}

                    <Button id="profilePic" onClick={() => setShow(true)}>
                      <img src={require('../../../resources/profile.png')}></img>
                    </Button>
                    <Modal
                      open={show}
                      onClose={() => setShow(false)}
                      aria-labelledby="modal-modal-title"
                      aria-describedby="modal-modal-description"
                    >
                      <Box sx={style}>
                        {username && userPerm && (
                          <>
                            <Typography id="modal-modal-description" sx={{ mt: 0 }}>
                              Username: {username ? username : "Not logged in"}
                            </Typography>
                            <Typography id="modal-modal-description" sx={{ mt: 0 }}>
                              Permission: {""}
                              {roles[userPerm]}
                            </Typography>
                          </>
                        )}
                        {(!username || !userPerm) && (
                          <>
                            <Typography id="modal-modal-description" sx={{ mt: 0 }}>
                              Not logged in
                            </Typography>
                          </>
                        )}
                      </Box>
                    </Modal>

                </Toolbar>
            </AppBar>
        </Box>
    );
}