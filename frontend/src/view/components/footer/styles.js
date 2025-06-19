import { Box, styled } from '@mui/system';
import GitHubIcon from '@mui/icons-material/GitHub';


export const FooterContainer = styled(Box)(({theme}) => ({
    paddingTop: "100px",
    paddingBottom: "30px",
    paddingLeft: "30px",
    backgroundColor: theme.palette.surface.dark,
    maxWidth: false,
    disableGutters: true,
    justifyContent: "center",
    alignItems: 'center',
    display: "grid"
}));


export const GitHubLinkIcon = styled(GitHubIcon)(({theme}) => ({
    '&:hover': {
        color: theme.palette.secondary.invertLight
    },

    transition: theme.transitions.medium + " !important"
}));