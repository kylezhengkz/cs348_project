import { useRef } from "react"
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useForm } from "react-hook-form"

export default function EditModal() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm()

  const onSubmit = (data) => console.log(data)

  return (
    <div className="modal fade" id="editModal" tabIndex="-1" aria-hidden="true">
      <div className="modal-dialog">
          <div className="modal-content">
              <div className="modal-header">
                  <h5 className="modal-title">Edit Room</h5>
                  <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div className="modal-body">
                 <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-group">
                        <label htmlFor="building" style={{ color: 'black' }}>Building</label>
                        <input type="text" id="building" name="building" className="form-control" {...register("building", { required: true })}></input>
                        {errors.building && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="room" style={{ color: 'black' }}>Room</label>
                        <input type="text" id="room" name="room" className="form-control" {...register("room", { required: true })}></input>
                        {errors.room && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="address" style={{ color: 'black' }}>Address</label>
                        <input type="text" id="address" name="address" className="form-control" {...register("address", { required: true })}></input>
                        {errors.building && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="city" style={{ color: 'black' }}>City</label>
                        <input type="text" id="city" name="city" className="form-control" {...register("city", { required: true })}></input>
                        {errors.city && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="country" style={{ color: 'black' }}>Country</label>
                        <input type="text" id="country" name="country" className="form-control" {...register("country", { required: true })}></input>
                        {errors.city && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="form-group mt-3">
                        <label htmlFor="postalCode" style={{ color: 'black' }}>Postal Code</label>
                        <input type="text" id="postalCode" name="postalCode" className="form-control" {...register("postalCode", { required: true })}></input>
                        {errors.city && <span className="text-danger">This field is required</span>}
                    </div>
                    <div className="modal-footer mt-5">
                        <Button variant="contained" type="submit">
                            Edit Room
                        </Button>
                    </div>
                </form>
              </div>
          </div>
      </div>
    </div>
  )
}
