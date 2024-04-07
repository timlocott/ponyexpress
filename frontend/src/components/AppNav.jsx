import { useAuth } from "../context/auth";
import { useUser } from "../context/user";

import { NavLink } from "react-router-dom";

// eslint-disable-next-line react/prop-types
function NavItem({to,name}) {
    return (
        <NavLink to={to} className="p-2 hover:bg-vanilla hover:text-wenge">
            {name}
        </NavLink>
    );
}

function AuthenticatedNavItems() {
    const user = useUser();

    return (
        <>
            <NavItem to="/" name="pony express"/>
            <div className="flex-1"></div>
            <NavItem to="/profile" name={user.username} />
        </>
    );
}

function UnauthenticatedNavItems() {
    return (
        <>
            <NavItem to="/" name="pony express" />
            <NavItem to="/login" name="login" />
        </>
    );
}

function AppNav() {
    const { isLoggedIn } = useAuth();

    return (
        <nav className="flex flex-row justify-between bg-wenge border-b-2 border-vanilla text-vanilla">
            {isLoggedIn ?
                <AuthenticatedNavItems /> :
                <UnauthenticatedNavItems />
            }
        </nav>
    );
}

export default AppNav;