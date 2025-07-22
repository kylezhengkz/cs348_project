import "./signup.css"
import { useForm, SubmitHandler } from "react-hook-form"
import { useNavigate } from "react-router-dom";

import { userService } from '../../../model/UserService';
import { useAuth } from "../../../wrappers/AuthContext"
import { USER_PERMS } from "../../../constants/authContants";

export function Signup() {

  const { setAuthUserId, setUsername, setUserPerm } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
    setError
  } = useForm()

  const navigate = useNavigate();

  async function createAccount(username, email, password) { // also manages the navigation logic
    let res = await userService.signup(username, email, password);
    console.log("Response", res)
    if (res["signupStatus"] === true) {
      setAuthUserId(res["userId"])
      setUsername(username)
      setUserPerm(USER_PERMS.USER)
      navigate("/home");
    } else {
        if (res["errorMessage"].includes("Username")) {
        setError("username", {
          type: "databaseError",
          message: res["errorMessage"]
        })
      } else if (res["errorMessage"].includes("Email")) {
        setError("email", {
          type: "databaseError",
          message: res["errorMessage"]
        })
      } else {
        setError("creationError", {
          type: "databaseError",
          message: res["errorMessage"]
        })
      }
    }
  }

  const onSubmit = async (data) => {
    console.log(data.username, data.email, data.password, data.passwordConfirm)
    if (data.password !== data.passwordConfirm) {
      setError("passwordConfirm", {
        type: "notMatch",
        message: "Passwords do not match",
      });
      return;
    }

    await createAccount(data.username, data.email, data.password);
  }

  return (
    <div className="container-sm mt-5 mb-5 pt-5 pb-5">
      <h1 className="text-center mt-3" style={{ color: 'white' }}>Sign up</h1>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group pt-3">
          <label htmlFor="username" style={{ color: 'white' }}>Username</label>
          <input type="text" id="username" name="username" className="form-control" {...register("username", { required: true })}></input>
          {errors.username?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.username?.type === "databaseError" && <span className="text-warning">{errors.username?.message}</span>}
        </div>

        <div className="form-group pt-3">
          <label htmlFor="email" style={{ color: 'white' }}>Email</label>
          <input type="text" id="email" name="email" className="form-control" {...register("email", { required: true })}></input>
          {errors.email?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.email?.type === "databaseError" && <span className="text-warning">{errors.email?.message}</span>}
        </div>
        
        <div className="form-group pt-3">
          <label htmlFor="password" style={{ color: 'white' }}>Password</label>
          <input type="password" id="password" name="password" className="form-control" {...register("password", { required: true, minLength: {value: 8, message: "Password must be at least 8 characters long"} })}></input>
          {errors.password?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.password?.type === "minLength" && <span className="text-warning">{errors.password?.message}</span>}
        </div>

        <div className="form-group pt-3">
          <label htmlFor="passwordConfirm" style={{ color: 'white' }}>Confirm Password</label>
          <input type="password" id="passwordConfirm" name="passwordConfirm" className="form-control" {...register("passwordConfirm", { required: true })}></input>
          {errors.passwordConfirm?.type === "required" && <span className="text-warning">This field is required</span>}
          {errors.passwordConfirm?.type === "notMatch" && <span className="text-warning">{errors.passwordConfirm?.message}</span>}
        </div>
        
        <div className="form-group pt-4 mx-auto text-center">
          <button type="submit" className="btn btn-primary">Sign up</button>
          <>
            {errors.creationError?.type === "databaseError" && (
              <>
                <br></br>
                <span className="text-warning">Unable to create account</span>
              </>
            )}
          </>
        </div>
      </form>
    </div>
  );
}
