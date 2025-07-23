import Button from '@mui/material/Button';
import { useForm } from "react-hook-form"

export default function AddRoomModal({onAdd}) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm()

  const onSubmit = (data) => {
    console.log(data)
    onAdd(data.roomName, data.capacity)
  }

  return (
    <div className="modal fade" id="addRoomModal" tabIndex="-1" aria-hidden="true">
      <div className="modal-dialog">
          <div className="modal-content">
              <div className="modal-header">
                  <h5 className="modal-title">Add Room</h5>
                  <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                 <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-group">
                        <label htmlFor="roomName" style={{ color: 'black' }}>Room Name</label>
                        <input type="text" id="roomName" name="buiroomNamelding" className="form-control" {...register("roomName", { required: true })}></input>
                        {errors.roomName && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="capacity" style={{ color: 'black' }}>Capacity</label>
                        <input type="number" id="capacity" name="capacity" className="form-control" {...register("capacity", { required: true })}></input>
                        {errors.capacity && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="modal-footer mt-5">
                        <Button variant="contained" type="submit">
                            Add Room
                        </Button>
                    </div>
                </form>
              </div>
          </div>
      </div>
    </div>
  )
}
