import { useContext } from "react";
import { AuthContext } from "./context/auth";
import { UserContext } from "./context/user";
import api from "./utils/api";

const useAPI = () => {
  const { token } = useAuth();
  return api(token);
}

const useAPIWithoutToken = () => {
  return api();
}

const useAuth = () => useContext(AuthContext);

const useUser = () => useContext(UserContext);

export {
  useAPI,
  useAPIWithoutToken,
  useAuth,
  useUser,
};