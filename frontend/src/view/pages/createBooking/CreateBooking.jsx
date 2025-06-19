import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { useRef, useState } from 'react';
import Modal from '@mui/material/Modal';

import { bookingService } from '../../../model/BookingService';


export function CreateBooking() {
    const userRef = useRef();
    const roomRef = useRef();
    const startDateTimeRef = useRef();
    const endDateTimeRef = useRef();
    const participantsRef = useRef();

    const bookSuccess = useRef(false);
    const bookResultMsg = useRef("");

    const [openModal, setOpenModal] = useState(false);


    function closeModal() {
        setOpenModal(false);
    }


    function bookRoom() {
        let userId = userRef.current.value;
        let roomId = roomRef.current.value;
        let startDateTime = startDateTimeRef.current.value;
        let endDateTime = endDateTimeRef.current.value;
        let participants = participantsRef.current.value;

        if (userId === "") userId = undefined;
        if (roomId === "") roomId = undefined;
        if (startDateTime === "") startDateTime = undefined;
        if (endDateTime === "") endDateTime = undefined;
        if (participants === "") participants = undefined;

        bookingService.bookRoom(userId, roomId, startDateTime, endDateTime, participants).then(res => {
            bookSuccess.current = res.data[0];
            bookResultMsg.current = res.data[1];
            setOpenModal(true);
        });
    }


    return (
        <Container className="mt-5 mb-5" maxWidth="xl">
            <Modal open={openModal}>
                <div className="modal" tabindex="-1" style={{display: "block"}}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h1 className="modal-title fs-5" id="alertPopupTitle">{(bookSuccess.current) ? "Booking Successful!" : "An error has occured during the booking"}</h1>
                                <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close" onClick={closeModal}>
                                    <i className="fas fa-times fa-lg popupExitBtnIcon"></i>
                                </button>
                            </div>
                            <div className="modal-body">
                                <p>{bookResultMsg.current}</p>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-primary" onClick={closeModal}>Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            </Modal>

            <Box minHeight="600px">
                <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Book a Room</Typography>

                <Box>
                    <Typography variant='subtitle1'>User Id</Typography>
                    <TextField label="User Id" variant="outlined" inputRef={userRef}></TextField>
                </Box>

                <Box className="mt-3">
                    <Typography variant='subtitle1'>Room Id</Typography>
                    <TextField label="Room Id" variant="outlined" inputRef={roomRef}></TextField>
                </Box>

                <Box className="mt-3" display={"flex"} gap={"30px"}>
                    <Box>
                        <Typography variant='subtitle1'>Start DateTime</Typography>
                        <TextField variant="outlined" type="datetime-local" inputRef={startDateTimeRef}></TextField>
                    </Box>

                    <Box>
                        <Typography variant='subtitle1'>End DateTime</Typography>
                        <TextField variant="outlined" type="datetime-local" inputRef={endDateTimeRef}></TextField>
                    </Box>
                </Box>

                <Box className="mt-3">
                    <Typography variant='subtitle1'>Participants</Typography>
                    <TextField label="Participants" variant="outlined" type="number" inputRef={participantsRef}></TextField>
                </Box>

                <Button variant="contained" className='mt-4' onClick={bookRoom}>Book Room</Button>
            </Box>
        </Container>
    );
}