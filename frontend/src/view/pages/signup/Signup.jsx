import "./signup.css"
import { useForm, SubmitHandler } from "react-hook-form"
import { useNavigate } from "react-router-dom";

import { userService } from '../../../model/UserService';
import { useAuth } from "../../../wrappers/AuthContext"

export function Signup() {

  const { setAuthUserId } = useAuth();

  async function createAccount(username, email, password) {
    let res = await userService.signup(username, email, password);
    console.log("Response", res)
    if (res[0] === true) {
      console.log(`Setting userId to ${res[2]}`)
      setAuthUserId(res[2])
    }
  }

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
    setError
  } = useForm()

  const navigate = useNavigate();

  const onSubmit = (data) => {
    console.log(data.username, data.email, data.password, data.passwordConfirm)
    if (data.password === data.passwordConfirm) {
      createAccount(data.username, data.email, data.password)
      navigate("/home")
      return
    }
    setError("passwordConfirm", {
      type: "not match",
      message: "Passwords do not match",
    })
  }

  return (
    <div className="container-sm mt-5 mb-5 pt-5 pb-5">
      <h1 className="text-center mt-3" style={{ color: 'white' }}>Sign up</h1>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group pt-3">
          <label htmlFor="username" style={{ color: 'white' }}>Username</label>
          <input type="text" id="username" name="username" className="form-control" {...register("username", { required: true })}></input>
          {errors.username && <span className="text-warning">This field is required</span>}
        </div>

        <div className="form-group pt-3">
          <label htmlFor="email" style={{ color: 'white' }}>Email</label>
          <input type="text" id="email" name="email" className="form-control" {...register("email", { required: true })}></input>
          {errors.email && <span className="text-warning">This field is required</span>}
        </div>
        
        <div className="form-group pt-3">
          <label htmlFor="password" style={{ color: 'white' }}>Password</label>
          <input type="password" id="password" name="password" className="form-control" {...register("password", { required: true })}></input>
          {errors.password && <span className="text-warning">This field is required</span>}
        </div>

        <div className="form-group pt-3">
          <label htmlFor="passwordConfirm" style={{ color: 'white' }}>Confirm Password</label>
          <input type="password" id="passwordConfirm" name="passwordConfirm" className="form-control" {...register("passwordConfirm", { required: true })}></input>
          {errors.passwordConfirm?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.passwordConfirm?.type === "not match" && <span className="text-warning">Password does not match</span>}
        </div>
        
        <div className="form-group pt-4 mx-auto text-center">
          <button type="submit" className="btn btn-primary">Sign up</button>
        </div>
      </form>
    </div>
  );
}
