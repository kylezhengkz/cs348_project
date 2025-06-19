import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { useRef, useState } from 'react';
import Modal from '@mui/material/Modal';

import { bookingService } from '../../../model/BookingService';


export function CancelBooking() {
    const userRef = useRef();
    const bookingRef = useRef();

    const bookSuccess = useRef(false);
    const bookResultMsg = useRef("");

    const [openModal, setOpenModal] = useState(false);


    function closeModal() {
        setOpenModal(false);
    }

    function cancelBooking() {
        let userId = userRef.current.value;
        let bookingId = bookingRef.current.value;

        if (userId === "") userId = undefined;
        if (bookingId === "") bookingId = undefined;

        bookingService.cancelBooking(userId, bookingId).then(res => {
            console.log("HELLO: ", res.data[0]);
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
                                <h1 className="modal-title fs-5" id="alertPopupTitle">{(bookSuccess.current) ? "Booking Cancelled!" : "An error has occured during the cancellation"}</h1>
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
                <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Cancel a Booking</Typography>

                <Box>
                    <Typography variant='subtitle1'>User Id</Typography>
                    <TextField label="User Id" variant="outlined" inputRef={userRef}></TextField>
                </Box>

                <Box className="mt-3">
                    <Typography variant='subtitle1'>Booking Id</Typography>
                    <TextField label="Booking Id" variant="outlined" inputRef={bookingRef}></TextField>
                </Box>

                <Button variant="contained" className='mt-4' onClick={cancelBooking}>Cancel Booking</Button>
            </Box>
        </Container>
    );
}