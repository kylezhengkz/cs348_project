import Typography from '@mui/material/Typography';
import { Container } from '@mui/material';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import { useRef, useState, useEffect } from 'react';
import { bookingService } from '../../../model/BookingService';
import { ReactDataTable } from '../../components/reactDataTable/ReactDataTable';
import 'bootstrap/dist/css/bootstrap.min.css';

const DUMMY_USER_ID = "6a51e4df-f4d8-4398-b603-5fd42c7738d0";

export function CancelBooking() {
    const bookSuccess = useRef(false);
    const bookResultMsg = useRef("");

    const [openModal, setOpenModal] = useState(false);
    const [futureBookings, setFutureBookings] = useState([]);

    function closeModal() {
        setOpenModal(false);
    }

    function handleCancelFromList(bookingId) {
        bookingService.cancelBooking(DUMMY_USER_ID, bookingId).then(res => {
            const [success, message] = res.data || [false, "Unexpected error"];
            alert(success ? "Booking cancelled!" : `Cancellation failed: ${message}`);

            if (success) {
                setFutureBookings(prev => prev.filter(b => b.bookingID !== bookingId));
            }
        });
    }

    useEffect(() => {
        bookingService.getFutureBookings(DUMMY_USER_ID).then(res => {
            const [success, data] = res.data || [];
            if (success) {
                setFutureBookings(data.map(b => ({
                    bookingID: b[0],
                    startTime: new Date(b[1]).toLocaleString(),
                    endTime: new Date(b[2]).toLocaleString(),
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
    }, []);

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
    }, [futureBookings]);

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
        </Container>
    );
}
