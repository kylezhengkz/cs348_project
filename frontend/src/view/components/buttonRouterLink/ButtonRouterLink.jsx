import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';


export function ButtonRouterLink({buttonProps, linkProps, children}) {
    if (linkProps === undefined) {
        linkProps = {};
    }

    if (linkProps["style"] === undefined) {
        linkProps["style"] = {};
    }

    linkProps["style"]["textDecoration"] = "none";

    return (
        <Button {...buttonProps}>
            <Link {...linkProps}>
                {children}
            </Link>
        </Button>
    );
}