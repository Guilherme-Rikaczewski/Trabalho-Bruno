import mainRoutes from "./MainRoutes";
import authRoutes from "./AuthRoutes";

const appRoutes = [
  ...mainRoutes,
  ...authRoutes
]

export default appRoutes;