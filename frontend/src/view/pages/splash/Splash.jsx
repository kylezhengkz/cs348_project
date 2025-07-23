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
        <div className="splashBackground">
            <div className="splashPanel">
                <div className="splashTopBar">
                    <Typography className="splashLogoText">CampusBooking</Typography>
                    <div className="splashNavBar">
                        <FeatureButtonLink buttonProps={{variant: "text"}} linkProps={{"to": "/signup"}}>Sign up</FeatureButtonLink>
                        <FeatureButtonLink buttonProps={{variant: "text"}} linkProps={{"to": "/login"}}>Login</FeatureButtonLink>
                    </div>
                </div>
                <div className="splashBody">
                    <div className="splashHeader">
                        <Typography className="splashHeaderText">Study. Meet. Chill.</Typography>
                        <Typography className="splashHeaderText">Find your space at UW.</Typography>
                    </div>
                    <Typography className="splashBodyText" style={{width: "60%"}}>
                        Tip: Appease campus geese with a selection of apples, grapes, earth worms, and duckweed!
                    </Typography>
                </div>
                <div className="splashBottomBar">
                    <FeatureButtonLink buttonProps={{
                            variant: "contained",
                            sx: {
                                background: 'linear-gradient(45deg, #996bfeff 30%, #9e64b0ff 90%)',
                                textTransform: 'none',
                                padding: '7px 23px',
                                marginBottom: '2rem',
                                boxShadow: '0 0 12px rgba(158, 100, 176, 0.6)',
                                transition: 'box-shadow 0.3s ease, background 0.3s ease',
                                '&:hover': {
                                    background: 'linear-gradient(45deg, #825bd7ff 30%, #a468b3ff 90%)',
                                    boxShadow: 'none',
                                },
                            }
                        }}
                        linkProps={{"to": "/login"}}
                    >
                        Get Started
                    </FeatureButtonLink>
                </div>
            </div>
        </div>
    );
}