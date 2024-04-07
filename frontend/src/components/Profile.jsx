import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
// import { useState, useEffect } from "react";

// import FormInput from "./FormInput";
import Button from "./Button";

function Profile() {
    const { logout } = useAuth();
    const user = useUser();

    return (
        <div className="flex flex-col justify-center w-96">
            <div className="flex flex-col justify-center border-2 border-vanilla rounded p-4 mb-4 divide-y divide-beige">
                <h2 className="text-xl text-darkSlateGray">details</h2>
                <div className="flex flex-row justify-between my-2">
                    <h3 className="text-verdigris">username</h3>
                    <h3 className="text-britishRacingGreen">{user.username}</h3>
                </div>
                <div className="flex flex-row justify-between my-2">
                    <h3 className="text-verdigris">email</h3>
                    <h3 className="text-britishRacingGreen">{user.email}</h3>
                </div>
                <div className="flex flex-row justify-between my-2">
                    <h3 className="text-verdigris">member since</h3>
                    <h3 className="text-britishRacingGreen">{new Date(user.created_at).toDateString()}</h3>
                </div>
            </div>
            <Button onClick={logout}>
                logout
            </Button>
        </div>
    );
}

export default Profile;