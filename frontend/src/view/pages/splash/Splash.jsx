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


export function Splash() {
    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h1" gutterBottom>Welcome</Typography>
                </Box>

                <Box justifyContent="center" display="flex" className="mt-3">
                    <Typography variant="p" gutterBottom>This is where the splash page should be. In the meantime you can explore the following function below</Typography>
                </Box>    

                <Box justifyContent="center" display="flex" className="mt-3" gap={"20px"}>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/signup"}}>Sign up</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/login"}}>login</FeatureButtonLink>
                </Box> 
            </Box>
        </Container>
    );
}