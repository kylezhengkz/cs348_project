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

import { buildingService } from '../../../model/BuildingService';
import { roomService } from '../../../model/RoomService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

import addIcon from "../../../resources/better_add_icon.png";

import "./ManageBuildings.css"

import "./AddRoomModal"

import { useNavigate } from "react-router-dom";
import AddRoomModal from './AddRoomModal';

export function ManageBuildings() {
    const { authUserId } = useAuth();
    const selectedBuildingId = useRef();
    const [data, setData] = useState([]);

    const buildingNameRef = useRef();
    const addressLine1Ref = useRef();
    const addressLine2Ref = useRef();
    const cityRef = useRef();
    const provinceRef = useRef();
    const countryRef = useRef();
    const postalCodeRef = useRef();

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    const navigate = useNavigate();

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    function getBuildings(setData, buildingName, addressLine1, addressLine2, city, province, country, postalCode) {
        buildingService.fetchBuildings(buildingName, addressLine1, addressLine2, city, province, country, postalCode).then(buildings => {
            console.log("BUILDINGS: ", buildings);
            setData(buildings);
        });
    }

    function filterBuildings() {
        console.log(cityRef.current)
        let buildingName = buildingNameRef.current.value;
        let addressLine1 = addressLine1Ref.current.value;
        let addressLine2 = addressLine2Ref.current.value;
        let city = cityRef.current.value;
        let province = provinceRef.current.value;
        let country = countryRef.current.value;
        let postalCode = postalCodeRef.current.value;

        if (buildingName === "") buildingName = undefined;
        if (addressLine1 === "") addressLine1 = undefined;
        if (addressLine2 === "") addressLine2 = undefined;
        if (city === "") city = undefined;
        if (province === "") province = undefined;
        if (country === "") country = undefined;
        if (postalCode === "") postalCode = undefined;

        getBuildings(setData, buildingName, addressLine1, addressLine2, city, province, country, postalCode);
    }

    async function onAdd(roomName, capacity) {
        try {
            const res = await roomService.addRoom(roomName, capacity, selectedBuildingId.current)
            console.log(res)
            if (res["addStatus"] === false) {
                setAlertSeverity("error");
                setAlertMessage(res["errorMessage"]);
                setAlertOpen(true);
            } else {
                setAlertSeverity("success");
                setAlertMessage("Successfully added room");
                setAlertOpen(true);
                getBuildings(setData)
            }
        } catch {
            setAlertSeverity("error");
            setAlertMessage("Unable to add room");
            setAlertOpen(true);
        } finally {
            const addRoomModal = bootstrap.Modal.getInstance(document.getElementById('addRoomModal'));
            console.log("CLOSING MODAL", addRoomModal)
            addRoomModal.hide();
        }
    }

    function handleOperationButtonClick(buildingId, operation) {
        selectedBuildingId.current = buildingId;
        console.log("clicked", buildingId);
        console.log("Check", selectedBuildingId.current);
        switch (operation) {
          case "add":
            const addRoomModal = new bootstrap.Modal(document.getElementById('addRoomModal'));
            addRoomModal.show()
            break
        }
    }

    const columns = [
        // {title: "Room Id", data: "roomID", width: "400px"},
        {title: "Building", data: "buildingName", width: "200px"},
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
                    <button class='action-btn' data-op='add' data-room-id='${row.buildingID}'>
                        <img id="add" src="${addIcon}"></img>
                    </button>
              </div>`
          );
        }
      }
    ];

    useEffect(() => {
        getBuildings(setData);
    }, []);
    
    useEffect(() => {
        const handleClick = (event) => {
            const target = event.target.closest('.action-btn');
            if (target && document.contains(target)) {
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
            <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Available Rooms</Typography>

            <Accordion className='mt-3'>
                <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1-content">
                    <Typography component="span">Filters</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Box>
                        <Box>
                            <TextField label="Building Name" variant="outlined" inputRef={buildingNameRef}></TextField>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <TextField label="Address Line 1" variant="outlined" inputRef={addressLine1Ref}></TextField>
                            </Box>

                            <Box>
                                <TextField label="Address Line 2" variant="outlined" inputRef={addressLine2Ref}></TextField>
                            </Box>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <TextField label="City" variant="outlined" inputRef={cityRef}></TextField>
                            </Box>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <TextField label="Province" variant="outlined" inputRef={provinceRef}></TextField>
                            </Box>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <TextField label="Country" variant="outlined" inputRef={countryRef}></TextField>
                            </Box>
                        </Box>

                        <Box className="mt-3" display={"flex"} gap={"30px"}>
                            <Box>
                                <TextField label="Postal Code" variant="outlined" inputRef={postalCodeRef}></TextField>
                            </Box>
                        </Box>

                        <Button variant="contained" className='mt-4' onClick={filterBuildings}>Filter</Button>
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

            <AddRoomModal onAdd={onAdd}></AddRoomModal>

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
