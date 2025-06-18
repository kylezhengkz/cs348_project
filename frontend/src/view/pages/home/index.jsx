import "./styles.css"

import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Box } from '@mui/material';
import { ButtonRouterLink } from '../../components/buttonRouterLink/ButtonRouterLink';



export function FeatureButtonLink({buttonProps, linkProps, children}) {
    if (linkProps === undefined) {
        linkProps = {};
    }

    linkProps["className"] = "featureButtonLink";

    return (
        <ButtonRouterLink buttonProps={buttonProps} linkProps={linkProps}>
            {children}
        </ButtonRouterLink>
    );
}


export function Home() {
    const apiURL = process.env.REACT_APP_API_URL;

    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h1" gutterBottom>This is the homepage</Typography>
                </Box>

                <Box justifyContent="center" display="flex" className="mt-3">
                    <Typography variant="p" gutterBottom>This is where the homepage should be. In the meantime you can explore the following function below: {apiURL}</Typography>
                </Box>    

                <Box justifyContent="center" display="flex" className="mt-3">
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "viewBooking"}}>View Available Rooms</FeatureButtonLink>
                </Box> 
            </Box>
        </Container>
    );
}