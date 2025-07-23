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

import { userService } from '../../../model/UserService';
import { bookingService } from '../../../model/BookingService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

import "./ViewAdminLog.css";

export function ViewAdminLog({mode = "book"}) {
    const { authUserId } = useAuth();
    const [data, setData] = useState([]);

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    function getAdminLog(setData) {
        userService.viewAdminLog(authUserId).then(adminLog => {
            console.log("Admin Log: ", adminLog);
            setData(adminLog);
        });
    }

    const columns = [
        // {title: "Room Id", data: "roomID", width: "400px"},
        {title: "logID", data: "logID", width: "200px"},
        {title: "userID", data: "userID", width: "200px"},
        {title: "roomID", data: "roomID", width: "200px"},
        {title: "action", data: "action", width: "200px"},
        {title: "Room", data: "roomName", width: "200px"},
        {title: "Capacity", data: "capacity", width: "200px"},
        {title: "Building", data: "buildingName", width: "200px"},
        {title: "Address", data: null,
                    render: function (data, type, row) {
                        return `${row.addressLine1 || ""} ${row.addressLine2 || ""}`.trim();
                }, width: "200px"},
        {title: "City", data: "city", width: "140px"},
        {title: "Country", data: "country", width: "140px"},
        {title: "Postal Code", data: "postalCode", width: "170px"}
    ];

    useEffect(() => {
        getAdminLog(setData);
    }, []);

    return (
        <Container maxWidth="xl">
            <Typography variant="h2" gutterBottom className='mt-5 mb-5'>Available Rooms</Typography>
          
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
