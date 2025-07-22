import "./styles.css"

import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Box } from '@mui/material';
import { ButtonRouterLink } from '../../components/buttonRouterLink/ButtonRouterLink';
import { useAuth } from '../../../wrappers/AuthContext';
import { USER_PERMS } from "../../../constants/authContants";


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
    const { userPerm } = useAuth();

    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h1" gutterBottom>This is the homepage</Typography>
                </Box>

                <Box justifyContent="center" display="flex" className="mt-3">
                    <Typography variant="p" gutterBottom>This is where the homepage should be. In the meantime you can explore the following function below</Typography>
                </Box>    

                <Box justifyContent="center" display="flex" className="mt-3" gap={"20px"}>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/viewBooking"}}>View/Book Rooms</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/cancelBooking"}}>View/Cancel Bookings</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/bookingHistory"}}>Booking History</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/dashboard"}}>My Dashboard</FeatureButtonLink>
                    { userPerm === USER_PERMS.ADMIN && (
                        <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/manageFacilities"}}>Administration</FeatureButtonLink>
                    )}
                </Box> 
            </Box>
        </Container>
    );
}