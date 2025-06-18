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

import { roomService } from '../../../model/RoomService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';


export function ViewBooking() {
    const [data, setData] = useState([]);

    const roomRef = useRef();
    const minCapactiyRef = useRef();
    const maxCapacityRef = useRef();
    const startTimeRef = useRef();
    const endTimeRef = useRef();


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


    const columns = [
        {title: "Building", data: "buildingName"},
        {title: "Room", data: "roomName"},
        {title: "Address Line 1", data: "addressLine1"},
        {title: "Address Line 2", data: "addressLine2"},
        {title: "City", data: "city"},
        {title: "Country", data: "country"},
        {title: "Postal Code", data: "postalCode"}
    ];

    useEffect(() => {
        getRooms(setData);
    }, []);

    return (
        <Container maxWidth="xl">
            <Typography variant="h2" gutterBottom className='mt-5'>This is the view booking page</Typography>

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
                                <Typography variant='subtitle1'>Start Time</Typography>
                                <TextField variant="outlined" inputRef={startTimeRef} type="datetime-local"></TextField>
                            </Box>

                            <Box>
                                <Typography variant='subtitle1'>End Time</Typography>
                                <TextField variant="outlined" inputRef={endTimeRef} type="datetime-local"></TextField>
                            </Box>
                        </Box>

                        <Button variant="contained" className='mt-4' onClick={filterRooms}>Filter</Button>
                    </Box>
                </AccordionDetails>
            </Accordion>

            <ReactDataTable data={data} columns={columns} tableContainerProps={{className: "mt-5"}}></ReactDataTable>
        </Container>
    );
}