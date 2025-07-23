import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Box } from '@mui/material';

import { useAuth } from "../../../wrappers/AuthContext";
import { ButtonRouterLink } from '../../components/buttonRouterLink/ButtonRouterLink';
import { USER_PERMS } from "../../../constants/authContants";import { Dashboard } from "../dashboard/Dashboard";

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


export function AdminPage() {
    const { username, userPerm } = useAuth();

    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" className="mt-5">
                    <Typography variant="h2" gutterBottom>Admin Page</Typography>
                </Box>

                <Box justifyContent="center" display="flex" className="mt-3" gap={"20px"}>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/manageRooms"}}>Manage Rooms</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/manageBuildings"}}>Manage Buildings</FeatureButtonLink>
                    <FeatureButtonLink buttonProps={{variant: "contained"}} linkProps={{"to": "/viewAdminLog"}}>My Admin Log</FeatureButtonLink>
                </Box>

            </Box>
        </Container>
    );
}