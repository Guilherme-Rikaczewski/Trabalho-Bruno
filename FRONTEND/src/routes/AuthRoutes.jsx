import Login from '../auth/pages/Login'
import { Register } from '../auth/pages/Register'

const authRoutes = [
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/register',
    element: <Register />
  }
]

export default authRoutes