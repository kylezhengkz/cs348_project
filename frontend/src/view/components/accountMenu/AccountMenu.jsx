
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Settings from '@mui/icons-material/Settings';
import Logout from '@mui/icons-material/Logout';
import { Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';


export function AccountMenu({username, logOutHandler, anchorEl, open, onClose}) {
    const navigate = useNavigate();

    return (
        <Menu
            anchorEl={anchorEl}
            id="account-menu"
            open={open}
            onClose={onClose}
            onClick={onClose}
            slotProps={{
            paper: {
                elevation: 0,
                sx: {
                overflow: 'visible',
                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                mt: 1.5,
                '& .MuiAvatar-root': {
                    width: 32,
                    height: 32,
                    ml: -0.5,
                    mr: 1,
                },
                },
            },
            }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 50 }}
        >
            <Box sx={{ px: 2, py: 3}}>
            <Typography sx={{fontSize: "18px", fontWeight: "bold", color: "var(--mui-palette-primary-main)" }}>Hello {username}!</Typography>
            </Box>
            <Divider />
            <MenuItem onClick={() => {
                onClose();
                navigate('/editAccount');
            }}>
                <ListItemIcon>
                    <Settings fontSize="small" />
                </ListItemIcon>
                Edit Account
            </MenuItem>
            <MenuItem onClick={logOutHandler}>
            <ListItemIcon>
                <Logout fontSize="small" />
            </ListItemIcon>
            Logout
            </MenuItem>
        </Menu>
    );
}