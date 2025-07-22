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
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

import "./ManageRooms.css";

import EditModal from './EditModal';
import DeleteModal from './DeleteModal';

import bookIcon from "../../../resources/booking_icon.jpg";
import editIcon from "../../../resources/edit_icon.png";
import garbageCan from "../../../resources/garbage_can.png";

export function ManageRooms() {
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
        console.log(startTime)
        console.log("HEHEHEHA", startTime)
        let endTime = endTimeRef.current.value;

        if (roomName === "") roomName = undefined;
        if (minCapacity === "") minCapacity = undefined;
        if (maxCapacity === "") maxCapacity = undefined;
        if (startTime === "") startTime = undefined;
        if (endTime === "") endTime = undefined;

        getRooms(setData, roomName, minCapacity, maxCapacity, startTime, endTime);
    }

    function handleOperationButtonClick(roomId, operation) {
        selectedRoomId.current = roomId;
        console.log("clicked", roomId);
        switch (operation) {
          case "edit":
            const editModal = new bootstrap.Modal(document.getElementById('editModal'));
            editModal.show();
            break
          case "delete":
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
            deleteModal.show();
            break
        }
    }

    async function deleteRoom() {
        const roomId = selectedRoomId.current;
        console.log("Deleting room with", roomId)

        try {
            const res = await roomService.deleteRoom(roomId)
            setAlertSeverity("success");
            setAlertMessage("Room deleted");
            setAlertOpen(true);
            getRooms(setData)
        } catch {
            setAlertSeverity("error");
            setAlertMessage("Unable to delete room");
            setAlertOpen(true);
        } finally {
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
            console.log("CLOSING MODAL", modal)
            modal.hide();
        }
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
            return (
                `<div id="imageWrapper">
                    <button class='action-btn' data-op='edit' data-room-id='${row.roomID}'>
                        <img id="edit" src="${editIcon}"></img>
                    </button>
                    <button class='action-btn' data-op='delete' data-room-id='${row.roomID}'>
                        <img id="delete" src="${garbageCan}"></img>
                    </button>
                </div>`
            );
        }
      }
    ];

    useEffect(() => {
        getRooms(setData)
    }, []);
    
    useEffect(() => {
        const handleClick = (event) => {
            const target = event.target.closest('.action-btn');
            if (target && document.contains(target)) {
                console.log(target)
                console.log(target.getAttribute('data-room-id'))
                const roomId = target.getAttribute('data-room-id');
                const operation = target.getAttribute('data-op');
                handleOperationButtonClick(roomId, operation);
            }
        };

        document.body.addEventListener('click', handleClick);
        return () => document.body.removeEventListener('click', handleClick);
    }, []);

    return (
        <Container maxWidth="xl">
            <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Manage Rooms</Typography>

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
                            scrollX: true
                        }}
                    />
                </Box>
            </Box>

            <EditModal></EditModal>
            <DeleteModal deleteRoom={deleteRoom}></DeleteModal>

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
