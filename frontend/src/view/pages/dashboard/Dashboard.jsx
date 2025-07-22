import React, { useEffect, useState } from 'react';
import Typography from '@mui/material/Typography';
import { Container, Box, CircularProgress } from '@mui/material';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { useAuth } from "../../../wrappers/AuthContext";
import { dashBoardService } from "../../../model/DashBoardService"; 


export function Dashboard({ containerProps }) {
    const { authUserId } = useAuth();
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [alertOpen, setAlertOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("info");

    const Alert = React.forwardRef(function Alert(props, ref) {
        return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    useEffect(() => {
        if (!authUserId) return;

        dashBoardService.getDashboardMetrics(authUserId)
            .then(res => {
                console.log("📦 Dashboard API response:", res.data);
                setMetrics(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Dashboard API error:", err);
                setAlertSeverity("error");
                setAlertMessage("Failed to load dashboard metrics.");
                setAlertOpen(true);
                setLoading(false);
            });
    }, [authUserId]);


    return (
        <Container maxWidth="md" {...containerProps}>
            <Typography variant="h3" className="mt-5 mb-4">📊 My Dashboard</Typography>

            {loading ? (
                <Box display="flex" justifyContent="center" mt={4}>
                    <CircularProgress />
                </Box>
            ) : (
                <Box>
                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Average Booking Duration</Typography>
                        <Typography variant="body1" className="mt-2">
                            {metrics?.avg_duration_mins != null ? `${metrics.avg_duration_mins} minutes` : "N/A"}
                        </Typography>
                    </Box>

                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, backgroundColor: '#f5f5f5' }}>
                        <Typography variant="h6">Most Booked Hour</Typography>
                        <Typography variant="body1" className="mt-2">
                            {metrics?.most_booked_hour || "N/A"}
                        </Typography>
                    </Box>
                </Box>
            )}

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
