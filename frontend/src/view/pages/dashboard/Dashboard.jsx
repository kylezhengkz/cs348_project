import React, { useEffect, useRef, useState } from 'react';
import Typography from '@mui/material/Typography';
import { Container, Box, CircularProgress } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import moment from 'moment';

import { useAuth } from "../../../wrappers/AuthContext";
import { dashBoardService } from "../../../model/DashBoardService"; 
import { Histogram } from '../../components/histogram/Histogram';
import { PopupInfo } from '../../components/popupInfo/PopupInfo';
import { DateTimeTools } from '../../../tools/DateTimeTools';


const RoomTimeOptions = {
    AllTime: "allTime",
    LastWeek: "lastWeek",
    LastMonth: "lastMonth",
    LastYear: "lastYear",
    Custom: "Custom"
}

const RoomTimeOptText = {
    [RoomTimeOptions.AllTime]: "All Time",
    [RoomTimeOptions.LastWeek]: "Last Week",
    [RoomTimeOptions.LastMonth]: "Last Month",
    [RoomTimeOptions.LastYear]: "Last Year"
}

const RoomQueryLimitOptions = {
    Top3: "Top 3",
    Top5: "Top 5",
    Top10: "Top 10",
    Top20: "Top 20",
    All: "All",
    Custom: "Custom"
}

const RoomQueryLimitCounts = {
    [RoomQueryLimitOptions.Top3]: 3,
    [RoomQueryLimitOptions.Top5]: 5,
    [RoomQueryLimitOptions.Top10]: 10,
    [RoomQueryLimitOptions.Top20]: 20,
    [RoomQueryLimitOptions.All]: null
}


export function Dashboard({ containerProps }) {
    const { authUserId } = useAuth();

    const [loading, setLoading] = useState(true);
    const [alertOpen, setAlertOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("info");

    const [metrics, setMetrics] = useState(null);
    const [roomFreqs, setRoomFreqs] = useState([]);

    const [roomTimeOpt, setRoomTimeOpt] = useState(RoomTimeOptions.AllTime);
    const [showRoomTimeSelect, setShowRoomTimeSelect] = useState(false);
    const [roomQueryLimitOpt, setRoomQueryLimitOpt] = useState(RoomQueryLimitOptions.Top10);
    const [showRoomQueryLimitSelect, setShowRoomQueryLimitSelect] = useState(false);
    const [roomFreqGraphTitle, setRoomFreqGraphTitle] = useState("");

    const roomFreqStartRef = useRef();
    const roomFreqEndRef = useRef();
    const roomFreqQueryLimitRef = useRef();


    // parseRoomFreqTimeRange(timeOpt, start, end): Parses the raw input for the time range
    //  in the room frequency graph
    function parseRoomFreqTimeRange(timeOpt, start, end) {
        let error = false;

        if (timeOpt === RoomTimeOptions.Custom) {
            let endDateTime = moment(end);
            let startDateTime = moment(start);

            error = endDateTime.isBefore(startDateTime);
            const errMsg = error ? "End datetime cannot be earlier than the start datetime" : "";

            return {error, range: [start, end], errMsg};
        } else if (timeOpt === RoomTimeOptions.AllTime) {
            return {error, range: [null, null]};
        }

        let endDateTime = moment();
        let startDateTime = null;

        if (timeOpt === RoomTimeOptions.LastWeek) {
            startDateTime = endDateTime.subtract(7, "days");
        } else if (timeOpt === RoomTimeOptions.LastMonth) {
            startDateTime = endDateTime.subtract(1, "months");
        } else if (timeOpt === RoomTimeOptions.LastYear) {
            startDateTime = endDateTime.subtract(1, "years");
        }

        endDateTime = moment();
        endDateTime = DateTimeTools.momentToStr(endDateTime);

        if (startDateTime !== null) {
            startDateTime = DateTimeTools.momentToStr(startDateTime);
        }

        return {error, range: [startDateTime, endDateTime]};
    }

    // parseRoomFreqQueryLimit(limitOpt, limit): Parses the raw input for the query limit in
    //  the room frequency graph
    function parseRoomFreqQueryLimit(limitOpt, limit) {
        let result = RoomQueryLimitCounts[limitOpt];

        if (result !== undefined) {
            return {error: false, limit: result};
        }

        try {
            result = parseInt(limit);
        } catch {
            return {error: true, errMsg: "Cannot parse the query limit to an integer"};
        }

        if (Number.isNaN(result)) {
            return {error: true, errMsg: "Query limit is not a number"};
        } else if (result < 0) {
            return {error: true, errMsg: "Query limit cannot be less than 0"};
        }

        return {error: false, limit: result};
    }

    // parseRoomFreqArgs(): Parses all the raw user input
    function parseRoomFreqArgs() {
        const startDateTime = roomFreqStartRef.current?.value;
        const endDateTime = roomFreqEndRef.current?.value;

        const parsedTimeRange = parseRoomFreqTimeRange(roomTimeOpt, startDateTime, endDateTime);
        if (parsedTimeRange.error) {
            setAlertSeverity("error");
            setAlertMessage(parsedTimeRange.errMsg);
            setAlertOpen(true);
            return {error: true};
        }

        const customQueryLimit = roomFreqQueryLimitRef.current?.value;
        const parsedQueryLimit = parseRoomFreqQueryLimit(roomQueryLimitOpt, customQueryLimit);
        if (parsedQueryLimit.error) {
            setAlertSeverity("error");
            setAlertMessage(parsedQueryLimit.errMsg);
            setAlertOpen(true);
            return {error: true};
        }

        return {error: false, args: [...(parsedTimeRange.range), parsedQueryLimit.limit]};
    }

    // getRoomFreqGraphTitle(startDateTime, endDateTime, queryLimit): Generates the title for the room frequency graph
    function getRoomFreqGraphTitle(startDateTime, endDateTime, queryLimit) {
        let countTitle = queryLimit !== null ? `Top ${queryLimit} ` : "";
        let title = `${countTitle}Most Frequent Booked Rooms`;

        if (roomTimeOpt === RoomTimeOptions.AllTime) {
            title = `${RoomTimeOptText[roomTimeOpt]} ${title}`;
            return title;

        } else if (roomTimeOpt === RoomTimeOptions.Custom) {
            const dateTimeFormat = "YYYY-MM-DD";
            const startTimeStr = DateTimeTools.momentToStr(moment(startDateTime), dateTimeFormat);
            const endTimeStr = DateTimeTools.momentToStr(moment(endDateTime), dateTimeFormat);

            title += ` from ${startTimeStr} to ${endTimeStr}`;
            return title;
        }

        title += ` in the ${RoomTimeOptText[roomTimeOpt]}`;
        return title;
    }

    // filterRoomFreqs(): Updates the room frequecy graph when the user decides to custom filter the graph
    function filterRoomFreqs() {
        const args = parseRoomFreqArgs();
        if (args.error) return;

        const roomFreqTitle = getRoomFreqGraphTitle(...args.args);
        setRoomFreqGraphTitle(roomFreqTitle);

        dashBoardService.getBookingFrequency(authUserId, ...args.args)
            .then(([roomFreqSuccess, roomFreqData] ) => {
            setRoomFreqs(roomFreqData);
        });
    }

    // compareRoomFreq(roomData1, roomData2): Order for the room frequency data to be
    //  displayed on the bar chart
    // Order is:
    //  1. Sort by frequency in descending order
    //  2. Sort by name in alphabetical order
    function compareRoomFreq(roomData1, roomData2) {
        const room1Freq = roomData1.bookingCount;
        const room2Freq = roomData2.bookingCount;

        if (room1Freq !== room2Freq) {
            return room2Freq - room1Freq;
        }

        const room1Name = roomData1.roomName;
        const room2Name = roomData2.roomName;

        if (room1Name > room2Name) {
            return 1;
        } else if (room1Name < room2Name) {
            return -1;
        }

        return 0;
    }


    useEffect(() => {
        if (!authUserId) return;

        const roomFreqArgs = parseRoomFreqArgs();
        const roomFreqTitle = getRoomFreqGraphTitle(...roomFreqArgs.args);
        setRoomFreqGraphTitle(roomFreqTitle);

        Promise.all([
            dashBoardService.getDashboardMetrics(authUserId), 
            dashBoardService.getBookingFrequency(authUserId, ...roomFreqArgs.args)
        ]).then(([metricsRes, roomFreqRes]) => {
            setMetrics(metricsRes.data);
            setLoading(false);

            const [roomFreqSuccess, roomFreqData] = roomFreqRes;
            setRoomFreqs(roomFreqData);
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
                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, mb: 3, backgroundColor: "var(--mui-palette-surface-tertiary)" }}>
                        <Typography variant="h6">Average Booking Duration</Typography>
                        <Typography variant="body1" className="mt-2">
                            {metrics?.avg_duration_mins != null ? `${metrics.avg_duration_mins} minutes` : "N/A"}
                        </Typography>
                    </Box>

                    <Box sx={{ border: '1px solid #ccc', borderRadius: 2, p: 3, backgroundColor: 'var(--mui-palette-surface-tertiary)' }}>
                        <Typography variant="h6">Most Booked Hour</Typography>
                        <Typography variant="body1" className="mt-2">
                            {metrics?.most_booked_hour || "N/A"}
                        </Typography>
                    </Box>
                    <Box sx={{ mt: 4, border: '1px solid #ccc', borderRadius: 2}}>
                        <Box sx={{px: 3, py: 4, backgroundColor: 'var(--mui-palette-surface-tertiary)'}}>
                            <Typography variant='h6'>Room Frequency</Typography>
                        </Box>

                        <Accordion sx={{mb: 4}}>
                            <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel1-content"
                            id="panel1-header"
                            >
                                <Typography component="span">Filters</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Box>
                                    <Box>
                                        <Box>
                                            <Typography variant='subtitle1'>Time Range Options</Typography>
                                            <Select
                                                value={roomTimeOpt}
                                                label="Time Option"
                                                onChange={(e) => {
                                                    const option = e.target.value;
                                                    setRoomTimeOpt(option);
                                                    setShowRoomTimeSelect(option == RoomTimeOptions.Custom);
                                                }}
                                                >
                                                <MenuItem value={RoomTimeOptions.LastWeek}>Last Week</MenuItem>
                                                <MenuItem value={RoomTimeOptions.LastMonth}>Last Month</MenuItem>
                                                <MenuItem value={RoomTimeOptions.LastYear}>Last Year</MenuItem>
                                                <MenuItem value={RoomTimeOptions.AllTime}>All Time</MenuItem>
                                                <MenuItem value={RoomTimeOptions.Custom}>Custom</MenuItem>
                                            </Select>
                                        </Box>
                                        <Box sx={{display: showRoomTimeSelect ? "flex" : "none" }} className="mt-3" gap={"30px"}>
                                            <Box>
                                                <Typography variant='subtitle2'>Start DateTime</Typography>
                                                <TextField variant="outlined" inputRef={roomFreqStartRef} type="datetime-local"></TextField>
                                            </Box>

                                            <Box>
                                                <Typography variant='subtitle2'>End DateTime</Typography>
                                                <TextField variant="outlined" inputRef={roomFreqEndRef} type="datetime-local"></TextField>
                                            </Box>
                                        </Box>
                                    </Box>
                                    <Box className="mt-5">
                                        <Typography variant='subtitle1'>Query Limit Options</Typography>
                                        <Box>
                                            <Select
                                                value={roomQueryLimitOpt}
                                                label="Query Limit Option"
                                                onChange={(e) => {
                                                    const option = e.target.value;
                                                    setRoomQueryLimitOpt(option);
                                                    setShowRoomQueryLimitSelect(option == RoomQueryLimitOptions.Custom);
                                                }}
                                                >
                                                <MenuItem value={RoomQueryLimitOptions.Top3}>Top 3</MenuItem>
                                                <MenuItem value={RoomQueryLimitOptions.Top5}>Top 5</MenuItem>
                                                <MenuItem value={RoomQueryLimitOptions.Top10}>Top 10</MenuItem>
                                                <MenuItem value={RoomQueryLimitOptions.Top20}>Top 20</MenuItem>
                                                <MenuItem value={RoomQueryLimitOptions.All}>All</MenuItem>
                                                <MenuItem value={RoomQueryLimitOptions.Custom}>Custom</MenuItem>
                                            </Select>
                                        </Box>
                                        <Box sx={{display: showRoomQueryLimitSelect ? "flex" : "none" }} className="mt-3" gap={"30px"}>
                                            <Box>
                                                <Typography variant='subtitle2'>Query Limit</Typography>
                                                <TextField variant="outlined" inputRef={roomFreqQueryLimitRef} type="number" min="0"></TextField>
                                            </Box>
                                        </Box>
                                    </Box>

                                    <Button variant="contained" className='mt-5' onClick={filterRoomFreqs}>Filter</Button>
                                </Box>
                            </AccordionDetails>
                        </Accordion>

                        {roomFreqs.length > 0 ? (
                            <Histogram figureProps={{className: "mt-4"}} data={roomFreqs} freqAtt="bookingCount" binAtt="roomID" 
                                binLabelAtt="roomName" textAtt="roomName" compareFunc={compareRoomFreq}
                                title={roomFreqGraphTitle} xAxisTitle="Frequency" yAxisTitle="Rooms">
                            </Histogram>
                        ) : (
                            <Box display="flex" justifyContent="center" sx={{py: 4}}>
                                <Typography variant='subtitle1'>No Rooms Available</Typography>
                            </Box>
                        )}
                    </Box>
                </Box>
            )}

            <PopupInfo open={alertOpen} onClose={() => setAlertOpen(false)} alertSeverity={alertSeverity}>
                {alertMessage}
            </PopupInfo>
        </Container>
    );
}
