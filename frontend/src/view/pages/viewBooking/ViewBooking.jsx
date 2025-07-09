/* global bootstrap */
import React from 'react';
import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useEffect, useState, useRef } from 'react';
import { useAuth } from "../../../wrappers/AuthContext";

import { roomService } from '../../../model/RoomService';
import { bookingService } from '../../../model/BookingService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

export function ViewBooking() {
    const { authUserId } = useAuth();
    const selectedRoomId = useRef();
    const [data, setData] = useState([]);

    const roomRef = useRef();
    const minCapactiyRef = useRef();
    const maxCapacityRef = useRef();
    const startTimeRef = useRef();
    const endTimeRef = useRef();

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    function getRooms(setData, roomName, minCapacity, maxCapacity, startTime, endTime) {
        roomService.getAvailable(roomName, minCapacity, maxCapacity, startTime, endTime).then(rooms => {
            console.log("ROOMS: ", rooms);
            setData(rooms);
        });
    }

    function filterRooms() {
        let roomName = roomRef.current.value;
        let minCapacity = minCapactiyRef.current.value;
        let maxCapacity = maxCapacityRef.current.value;
        let startTime = startTimeRef.current.value;
        let endTime = endTimeRef.current.value;

        if (roomName === "") roomName = undefined;
        if (minCapacity === "") minCapacity = undefined;
        if (maxCapacity === "") maxCapacity = undefined;
        if (startTime === "") startTime = undefined;
        if (endTime === "") endTime = undefined;

        getRooms(setData, roomName, minCapacity, maxCapacity, startTime, endTime);
    }

    function handleBookButtonClick(roomId) {
        
        selectedRoomId.current = roomId;
        console.log("clicked", roomId);
        const modal = new bootstrap.Modal(document.getElementById('bookModal'));
        modal.show();
    }

    async function submitBooking() {

        const roomId = selectedRoomId.current;
        const startTime = startTimeRef.current.value;
        const endTime = endTimeRef.current.value;
        const participants = minCapactiyRef.current.value;

        if (!startTime || !endTime) {
            alert("Please provide both start and end time.");
            return;
        }

        try {
            const res = await bookingService.bookRoom(authUserId, roomId, startTime, endTime, participants);

          
            const { success, message } = res.data || {};

            if (success) {
              setAlertSeverity("success");
              setAlertMessage("Booking successful!");
            } else {
              setAlertSeverity("error");
              setAlertMessage("Booking failed: " + (message || "Unknown error"));
            }
            setAlertOpen(true);
            } catch (error) {
            console.error("Booking request failed:", error);

                if (error.response && error.response.data && error.response.data.message) {
                    setAlertMessage("Booking failed: " + error.response.data.message);
                } else {
                    setAlertMessage("Booking failed due to a server error.");
                }

             setAlertSeverity("error");
            setAlertOpen(true);
            }

        // Close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('bookModal'));
        modal.hide();

        document.body.classList.remove('modal-open');
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());
    }


    const columns = [
        // {title: "Room Id", data: "roomID", width: "400px"},
        {title: "Building", data: "buildingName", width: "200px"},
        {title: "Room", data: "roomName", width: "200px"},
        {title: "Address", data: null,
                    render: function (data, type, row) {
                        return `${row.addressLine1 || ""} ${row.addressLine2 || ""}`.trim();
                }, width: "200px"},
        {title: "City", data: "city", width: "140px"},
        {title: "Country", data: "country", width: "140px"},
        {title: "Postal Code", data: "postalCode", width: "170px"},
        {
        title: "Actions",
        data: null,
        width: "150px",
        render: function (data, type, row) {
    return `<button 
        class='book-btn'
        data-room-id='${row.roomID}' 
        style="
            min-width: 150px;
            padding: 6px 12px;
            background-color: #9b5aa7;
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;"
        onmouseover="this.style.backgroundColor='transparent'; this.style.color='#9b5aa7';"
        onmouseout="this.style.backgroundColor='#9b5aa7'; this.style.color='white';"
    >Book</button>`;
}
    }
    ];

    useEffect(() => {
        getRooms(setData);
    }, []);
    useEffect(() => {
    const wrapper = document.querySelector('#DataTables_Table_0_wrapper');
    console.log("Wrapper found?", wrapper);

    const handleClick = (event) => {
        const target = event.target.closest('.book-btn');
        if (target) {
            const roomId = target.getAttribute('data-room-id');
            console.log("CLICK DETECTED:", roomId);
            handleBookButtonClick(roomId);
        }
    };

    if (wrapper) {
        wrapper.addEventListener('click', handleClick);
    }

    return () => {
        if (wrapper) {
            wrapper.removeEventListener('click', handleClick);
        }
    };
}, [data]);

    return (
        <Container maxWidth="xl">
            <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Available Rooms</Typography>

            <Accordion className='mt-3'>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1-content">
                    <Typography component="span">Filters</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Box>
                        <Box>
                            <Typography variant='subtitle1'>Room Name</Typography>
                            <TextField label="Room Name" variant="outlined" inputRef={roomRef}></TextField>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <Typography variant='subtitle1'>Min Capacity</Typography>
                                <TextField label="Minimum Capacity" variant="outlined" inputRef={minCapactiyRef} type="number"></TextField>
                            </Box>

                            <Box>
                                <Typography variant='subtitle1'>Max Capacity</Typography>
                                <TextField label="Maximum Capacity" variant="outlined" inputRef={maxCapacityRef} type="number"></TextField>
                            </Box>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <Typography variant='subtitle1'>Start DateTime</Typography>
                                <TextField variant="outlined" inputRef={startTimeRef} type="datetime-local"></TextField>
                            </Box>

                            <Box>
                                <Typography variant='subtitle1'>End DateTime</Typography>
                                <TextField variant="outlined" inputRef={endTimeRef} type="datetime-local"></TextField>
                            </Box>
                        </Box>

                        <Button variant="contained" className='mt-4' onClick={filterRooms}>Filter</Button>
                    </Box>
                </AccordionDetails>
            </Accordion>

          
            <Box display="flex" justifyContent="center">
                <Box className="mt-5 mb-5" sx={{ width: '100%' }}>
                    <ReactDataTable
                        data={data}
                        columns={columns}
                        tableContainerProps={{ style: { width: '100%' } }}
                        dataTableKwargs={{
                            autoWidth: false,
                            scrollX: true, 
                            drawCallback: function () {
                                const buttons = document.querySelectorAll('.book-btn');
                                buttons.forEach(button => {
                                    button.onclick = (e) => {
                                        const roomId = button.getAttribute('data-room-id');
                                        handleBookButtonClick(roomId);
                                    };
                                });
                            }
                        }}
                    />
                </Box>
            </Box>

            <div className="modal fade" id="bookModal" tabIndex="-1" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Book Room</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            <TextField
                                fullWidth
                                label="Start Time"
                                type="datetime-local"
                                inputRef={startTimeRef}
                                InputLabelProps={{ shrink: true }}
                            />
                            <TextField
                                fullWidth
                                className="mt-3"
                                label="End Time"
                                type="datetime-local"
                                inputRef={endTimeRef}
                                InputLabelProps={{ shrink: true }}
                            />
                            <TextField
                                fullWidth
                                className="mt-3"
                                label="Participants"
                                inputRef={minCapactiyRef}
                                type="number"
                            />
                        </div>
                        <div className="modal-footer">
                            <Button variant="contained" onClick={submitBooking}>
                                Confirm Booking
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
            <Snackbar open={alertOpen} autoHideDuration={5000} onClose={() => setAlertOpen(false)}>
  <Alert
    onClose={() => setAlertOpen(false)}
    severity={alertSeverity}
    sx={{ width: '100%', backgroundColor: '#9b5aa7', color: 'white' }}
  >
    {alertMessage}
  </Alert>
</Snackbar>
        </Container>
    );
}
