import { useRef, useEffect } from "react"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function EditModal({
    roomName,
    capacity,
    editRoom
}) {

    const roomNameRef = useRef();
    const capacityRef = useRef();

    const submitEdit = () => {
        console.log("EDIT SUBMITTED")
        console.log(roomNameRef.current.value)
        console.log(capacityRef.current.value)
        editRoom(roomNameRef.current.value, capacityRef.current.value)
    }

    useEffect(() => {
        console.log("IN EDIT MODAL")
        console.log(roomName)
        console.log(capacity)

        roomNameRef.current.value = roomName
        capacityRef.current.value = capacity
    }, [roomName, capacity])

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
                      label="Room Name"
                      inputRef={roomNameRef}
                      InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                      fullWidth
                      className="mt-3"
                      label="Capacity"
                      inputRef={capacityRef}
                      type="number"
                      InputLabelProps={{ shrink: true }}
                  />
              </div>
              <div className="modal-footer">
                  <Button variant="contained" onClick={() => submitEdit()}>
                    Edit
                  </Button>
              </div>
          </div>
      </div>
    </div>
  )
}
