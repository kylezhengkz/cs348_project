import { Typography, Box } from "@mui/material";
import Link from '@mui/material/Link';

import { FooterContainer, GitHubLinkIcon } from "./styles";



export function Footer() {
    return (
        <div>
            <FooterContainer>
                <Box alignItems="center">
                    <Box display="flex" gap="10px" justifyContent="center" fontSize="18px">
                        <Typography variant="p" color="secondary.light" fontWeight="bold">Github: </Typography> 
                        <Link href="https://github.com/kylezhengkz/cs348_project/tree/main"><GitHubLinkIcon color="secondary" /></Link>
                    </Box>

                    <Box display="flex" gap="10px" justifyContent="center" sx={{mt: 2}}>
                        <Typography color="primary.light" fontWeight="bold" fontSize="12px">Made by:</Typography>
                        <Typography color="primary.light" fontSize="12px">
                            Alex Au, Anika Awasthi, Ananya Ohrie, 
                            <Link href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" underline="none" color="inherit"> Anthony Tieu</Link>
                            , Kyle Zheng
                        </Typography>
                    </Box>
                </Box>
            </FooterContainer>
        </div>
    );
}