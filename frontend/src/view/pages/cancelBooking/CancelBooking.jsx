import React from 'react';
import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import { useRef, useState, useEffect, useCallback } from 'react';
import { bookingService } from '../../../model/BookingService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import { useAuth } from "../../../wrappers/AuthContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';


export function CancelBooking() {
    const { authUserId } = useAuth();
    const bookSuccess = useRef(false);
    const bookResultMsg = useRef("");

    const [openModal, setOpenModal] = useState(false);
    const [futureBookings, setFutureBookings] = useState([]);

    const [alertOpen, setAlertOpen] = useState(false);
    const [alertSeverity, setAlertSeverity] = useState("info");
    const [alertMessage, setAlertMessage] = useState("");

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    function closeModal() {
        setOpenModal(false);
    }

    const handleCancelFromList = useCallback((bookingId) => {
        bookingService.cancelBooking(authUserId, bookingId).then(res => {
            const { success, message } = res.data || {};
            if (success) {
                setAlertSeverity("success");
                setAlertMessage("Booking cancelled successfully!");
                setFutureBookings(prev => prev.filter(b => b.bookingID !== bookingId));
            } else {
                setAlertSeverity("error");
                setAlertMessage("Cancellation failed: " + message);
            }
            setAlertOpen(true);
        });
    }, [authUserId]);

    useEffect(() => {
        if (!authUserId) return;
        bookingService.getFutureBookings(authUserId).then(res => { //------------
            const [success, data] = res.data || [];
            if (success) {
                setFutureBookings(data.map(b => ({
                    bookingID: b[0],
                    startTime: new Date(b[1]).toLocaleString("en-US", { timeZone: "UTC" }),
                    endTime: new Date(b[2]).toLocaleString("en-US", { timeZone: "UTC" }),
                    roomName: b[3],
                    address: b[4],
                    buildingName: b[5],
                    city: b[6],
                    country: b[7],
                })));
            } else {
                console.error("Failed to fetch bookings");
            }
        });
    }, [authUserId]);

    const columns = [
        { title: "Building", data: "buildingName", width: "200px" },
        { title: "Room", data: "roomName", width: "150px" },
        { title: "Address", data: "address", width: "200px" },
        { title: "City", data: "city", width: "140px" },
        { title: "Country", data: "country", width: "140px" },
        { title: "Start Time", data: "startTime", width: "200px" },
        { title: "End Time", data: "endTime", width: "200px" },
        {
            title: "Actions",
            data: null,
            width: "120px",
            render: function (data, type, row) {
                return `<button 
                    class='cancel-btn'
                    data-booking-id='${row.bookingID}' 
                    style="
                    min-width: 120px;
                    padding: 6px 12px;
                    background-color: #9b5aa7;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: 500;
                    transition: all 0.3s ease;"
                    onmouseover="this.style.backgroundColor='transparent'; this.style.color='#9b5aa7';"
                    onmouseout="this.style.backgroundColor='#9b5aa7'; this.style.color='white';"
                >Cancel</button>`;
            }

        }
    ];

    useEffect(() => {
        const wrapper = document.querySelector('#DataTables_Table_0_wrapper');

        const handleClick = (event) => {
            const target = event.target.closest('.cancel-btn');
            if (target) {
                const bookingId = target.getAttribute('data-booking-id');
                handleCancelFromList(bookingId);
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
    }, [futureBookings, handleCancelFromList]);

    return (
        <Container className="mt-5 mb-5" maxWidth="xl">
            <Modal open={openModal}>
                <div className="modal" tabIndex="-1" style={{ display: "block" }}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h1 className="modal-title fs-5" id="alertPopupTitle">
                                    {(bookSuccess.current)
                                        ? "Booking Cancelled!"
                                        : "An error has occurred during the cancellation"}
                                </h1>
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
                <Typography variant="h2" gutterBottom className="mt-5 mb-5">Your Future Bookings</Typography>

                <ReactDataTable
                    data={futureBookings}
                    columns={columns}
                    tableContainerProps={{ className: "mt-3 mb-5" }}
                    dataTableKwargs={{
                        autoWidth: false,
                        drawCallback: function () {
                            const buttons = document.querySelectorAll('.cancel-btn');
                            buttons.forEach(button => {
                                button.onclick = (e) => {
                                    const bookingId = button.getAttribute('data-booking-id');
                                    handleCancelFromList(bookingId);
                                };
                            });
                        }
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
