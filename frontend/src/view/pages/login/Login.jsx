import "./login.css"
import { useForm, SubmitHandler } from "react-hook-form"
import { useNavigate } from "react-router-dom";

import { userService } from '../../../model/UserService';
import { useAuth } from "../../../wrappers/AuthContext"

export function Login() {

  const { setAuthUserId, setUsername, setUserPerm } = useAuth();

  async function myLogin(username, password) {
    let res = await userService.login(username, password);
    console.log("Response", res)
    if (res["loginStatus"] === true) {
      setAuthUserId(res["userId"]);
      setUsername(username)
      setUserPerm(res["permLevel"]);
      return true;
    } else {
      console.log("Returning false")
      return false;
    }
  }

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setError
  } = useForm()

  const navigate = useNavigate();

  const onSubmit = async (data) => {
    console.log(data.username, data.password);
    let status = await myLogin(data.username, data.password)
    console.log(status)
    if (status) {
      navigate("/home");
      return
    }
    setError("password", {
      type: "incorrectCredentials",
      message: "Incorrect credentials"
    })
  }

  return (
    <div className="container-sm mt-5 mb-5 pt-5 pb-5">
      <h1 className="text-center mt-3" style={{ color: 'white' }}>Login</h1>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group pt-3">
          <label htmlFor="username" style={{ color: 'white' }}>Username</label>
          <input type="text" id="username" name="username" className="form-control" {...register("username", { required: true })}></input>
          {errors.username && <span className="text-warning">This field is required</span>}
        </div>
        <div className="form-group pt-3">
          <label htmlFor="password" style={{ color: 'white' }}>Password</label>
          <input type="password" id="password" name="password" className="form-control" {...register("password", { required: true })}></input>
          {errors.password?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.password?.type === "incorrectCredentials" && <span className="text-warning">Incorrect credentials</span>}
        </div>
        <div className="form-group pt-4 mx-auto text-center">
          <button type="submit" className="btn btn-primary">Login</button>
        </div>
      </form>
    </div>
  );
}
