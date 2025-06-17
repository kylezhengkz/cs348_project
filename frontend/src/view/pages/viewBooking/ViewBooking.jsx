import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';

import { roomService } from '../../../model/RoomService';


export function ViewBooking() {
    const temp = roomService.getAvailable()
        .then(response => console.log(response))
        .catch(error => console.error(error));


    return (
        <Container>
            <Typography variant="h1" gutterBottom>This is the view booking page</Typography>
        </Container>
    );
}