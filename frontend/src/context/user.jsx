/* eslint-disable react/prop-types */
/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext } from "react";
import { useQuery  } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./auth";

const UserContext = createContext();

function UserProvider({ children }) {
    const { isLoggedIn, logout, token } = useAuth();
    const navigate = useNavigate();

    const { data } = useQuery({
        queryKey: ["users", token],
        enabled: isLoggedIn,
        staleTime: Infinity,
        queryFn: () => (
            fetch(
                "http://127.0.0.1:8000/users/me",
                {
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                    },
                },
            ).then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    logout();
                    navigate("/login");
                }
            })
        ),
    });

    const emptyUser = { id: 0, email: "", username: "loading" }

    return (
        <UserContext.Provider value={data?.user || emptyUser}>
            {children}
        </UserContext.Provider>
    );
}

const useUser = () => useContext(UserContext);

export { UserProvider, useUser }
