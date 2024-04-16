import { useAuth } from "./context/auth";
import api from "./utils/api";

const useAPI = () => {
  const { token } = useAuth();
  return api(token);
}

const useAPIWithoutToken = () => {
  return api();
}


export {
  useAPI,
  useAPIWithoutToken,
};