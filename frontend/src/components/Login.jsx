/* eslint-disable react/no-unescaped-entities */
/* eslint-disable react/prop-types */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";
import FormInput from "./FormInput";
import Button from "./Button";
import { useAPIWithoutToken } from "../hooks";

function Error({ message }) {
    if(message === "") {
        return <></>;
    }
    return (
        <div>
            {message}
        </div>
    )
}

function Registration() {
    return (
        <div className="flex flex-row justify-between mt-6 text-sm">
            <div className="text-verdigris mr-6">
                don't have an account?
            </div>
            <Link to="/register">
                <a className="text-britishRacingGreen hover:text-tomato">
                    create an account
                </a>
            </Link>
        </div>
    )
}

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const { login } = useAuth();
    const api = useAPIWithoutToken();

    const disabled = username === "" || password === "";

    const onSubmit = (e) => {
        e.preventDefault();

        // fetch(
        //     "http://127.0.0.1:8000/auth/token",
        //     {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/x-www-form-urlencoded",
        //         },
        //         body: new URLSearchParams({ username, password }),
        //     },
        // ).then((response) => {
        //     if (response.ok){
        //         response.json().then(login).then(() => {navigate("/")});
        //     } else if (response.status === 401) {
        //         response.json().then((data) => {
        //             setError(data.detail.error_description);
        //         });
        //     } else {
        //         setError("error logging in");
        //     }
        // });

        api.postForm("/auth/token", { username, password })
            .then((response) => {
                if (response.ok){
                    response.json().then(login).then(() => {navigate("/")});
                } else if (response.status === 401) {
                    response.json().then((data) => {
                        setError(data.detail.error_description);
                    });
                } else {
                    setError("error logging in");
                }
            });
    }

    return (
        <div className="flex flex-col justify-center w-96">
            <form onSubmit={onSubmit} className="border-vanilla border-2 rounded min-h-min p-4">
                <FormInput type="text" name="username" setter={setUsername} />
                <FormInput type="password" name="password" setter={setPassword} />
                <Button type="submit" disabled={disabled}>
                    login
                </Button>
                <Error message={error} />
            </form>
            <Registration />
        </div>
    )
 }

export default Login;