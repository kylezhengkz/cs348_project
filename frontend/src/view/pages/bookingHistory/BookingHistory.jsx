import React from 'react';
import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import Box from '@mui/material/Box';
import { useState, useEffect } from 'react';
import { bookingService } from '../../../model/BookingService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import { useAuth } from "../../../wrappers/AuthContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';


export function BookingHistory() {
    const { authUserId } = useAuth();
    const [futureBookings, setFutureBookings] = useState([]);

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });


    useEffect(() => {
        if (!authUserId) return;
        bookingService.getBookingsAndCancellations(authUserId).then(res => { //------------
            const [success, data] = res.data || [];
            if (success) {
                console.log("Raw booking data:", res.data);
                setFutureBookings(data.map(b => ({
                    bookingID: b[0],
                    userID: b[1],
                    roomID: b[2],
                    bookDateTime: new Date(b[3]).toLocaleString("en-US", { timeZone: "UTC" }),
                    startTime: new Date(b[4]).toLocaleString("en-US", { timeZone: "UTC" }),
                    endTime: new Date(b[5]).toLocaleString("en-US", { timeZone: "UTC" }),
                    participants: b[6],
                    roomName: b[7],
                    buildingName: b[8],
                    address: b[9],
                    city: b[10],
                    country: b[11],
                    cancelled: b[12],
                })));
            } else {
                console.error("Failed to fetch bookings");
            }
        });
    }, [authUserId]);

    const columns = [
        { title: "Booking Time", data: "bookDateTime", width: "200px"},
        { title: "Start Time", data: "startTime", width: "200px"},
        { title: "End Time", data: "endTime", width: "200px"},
        { title: "Participants", data: "participants", width: "100px"},
        { title: "Room Name", data: "roomName", width: "100px"},
        { title: "Building", data: "buildingName", width: "200px"},
        { title: "Address", data: "address", width: "200px"},
        { title: "City", data: "city", width: "100px"},
        { title: "Country", data: "country", width: "100px"},
        {
            title: "Cancelled",
            data: "cancelled",
            width: "100px",
            render: function (data) {
                return data ? "Yes" : "No";
            }
        },
    ];

    return (
        <Container className="mt-5 mb-5" maxWidth="xl">
            <Box sx={{minHeight: "80vh"}}>
                <Typography variant="h2" gutterBottom className="mt-5 mb-5">Your Booking History</Typography>
                <ReactDataTable
                    data={futureBookings}
                    columns={columns}
                    tableContainerProps={{ className: "mt-3 mb-5" }}
                    dataTableKwargs={{
                        autoWidth: false,
                    }}
                />
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
