import { useRef } from "react"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function EditModal() {
  const startTimeRef = useRef();
  const endTimeRef = useRef();
  const participants = useRef();

  return (
    <div className="modal fade" id="editModal" tabIndex="-1" aria-hidden="true">
      <div className="modal-dialog">
          <div className="modal-content">
              <div className="modal-header">
                  <h5 className="modal-title">Edit Room</h5>
                  <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                  <TextField
                      fullWidth
                      label="Start Time"
                      type="datetime-local"
                      inputRef={startTimeRef}
                      InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                      fullWidth
                      className="mt-3"
                      label="End Time"
                      type="datetime-local"
                      inputRef={endTimeRef}
                      InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                      fullWidth
                      className="mt-3"
                      label="Participants"
                      inputRef={participants}
                      type="number"
                  />
              </div>
              <div className="modal-footer">
                  <Button variant="contained" onClick={() => {}}>
                      Confirm Booking
                  </Button>
              </div>
          </div>
      </div>
    </div>
  )
}
