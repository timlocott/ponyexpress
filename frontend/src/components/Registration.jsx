/* eslint-disable react/prop-types */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import FormInput from "../components/FormInput";
import Button from "../components/Button";

function Error({ message }) {
    if (message === "") {
        return <></>;
    }
    return (
        <div>
            {message}
        </div>
    )
}

function LoginLink() {
    return (
        <div className="flex flex-row justify-between mt-6 text-sm">
            <div className="text-verdigris mr-6">
                already have an account?
            </div>
            <Link to="/login">
                <a className="text-britishRacingGreen hover:text-tomato">
                    login
                </a>
            </Link>
        </div>
    )
}

function Registration() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const disabled = username === "" || email === "" || password === "";

    const onSubmit = (e) => {
        e.preventDefault();

        fetch(
            "http://127.0.0.1:8000/auth/registration",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, email, password}),
            },
        ).then((response) => {
            if (response.ok) {
                navigate("/login");
            } else if (response.status === 422) {
                response.json().then((data) => {
                    setError(data.detail.entity_field + " already taken");
                });
            } else {
                setError("error loggin in")
            }
        });
    }

    return (
        <div className="flex flex-col justify-center w-96">
            <form onSubmit={onSubmit} className="border-vanilla border-2 rounded min-h-min p-4"> 
                <FormInput type="text" name="username" setter={setUsername} />
                <FormInput type="email" name="email" setter={setEmail} />
                <FormInput type="password" name="password" setter={setPassword} />
                <Button type="submit" disabled={disabled}>
                    register
                </Button>
                <Error message={error} />
            </form>
            <LoginLink />
        </div>
    )
}

export default Registration;