import { Snackbar } from "@mui/material";
import Alert from '@mui/material/Alert';


export function PopupInfo({children, open, onClose, alertSeverity="info"}) {
    return (
        <Snackbar open={open} autoHideDuration={5000} onClose={onClose}>
          <Alert onClose={onClose} severity={alertSeverity}
            sx={{ width: '100%' }}>
            {children}
          </Alert>
        </Snackbar>
    );
}