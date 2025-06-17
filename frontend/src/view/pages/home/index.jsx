import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Box } from '@mui/material';
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';


export function Home() {
    const apiURL = process.env.REACT_APP_API_URL;

    return (
        <Container>
            <Box minHeight="600px">
                <Box justifyContent="center" display="flex" mt="50px">
                    <Typography variant="h1" gutterBottom>This is the homepage</Typography>
                </Box>

                <Box justifyContent="center" display="flex" mt="15px">
                    <Typography variant="p" gutterBottom>This is where the homepage should be. In the meantime you can explore the following function below: {apiURL}</Typography>
                </Box>    

                <Box justifyContent="center" display="flex" mt="15px">
                    <Button variant="contained">
                        <Link to="viewBooking">View Available Rooms</Link>
                    </Button>
                </Box> 
            </Box>
        </Container>
    );
}