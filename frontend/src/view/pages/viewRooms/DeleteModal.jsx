import Button from '@mui/material/Button';

export default function DeleteModal({deleteRoom}) {
  return (
    <div className="modal fade" id="deleteModal" tabIndex="-1" aria-hidden="true">
      <div className="modal-dialog">
          <div className="modal-content">
              <div className="modal-header">
                  <h5 className="modal-title">Book Room</h5>
                  <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                Are you sure you want to delete this room?
              </div>
              <div className="modal-footer">
                <Button variant="contained" type="submit" onClick={deleteRoom}>
                    Delete
                </Button>
            </div>
          </div>
      </div>
    </div>
  )
}
