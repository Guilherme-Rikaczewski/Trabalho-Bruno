import { useEffect, useState } from 'react';
import { useLocation, useNavigate, useRoutes } from 'react-router-dom';
import { refresh } from './auth/services/authService.js';
import appRoutes from './routes/AppRoutes.jsx';

const AUTH_ROUTES = ['/login', '/register']

const App = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const [loading, setLoading] = useState(false)

  const element = useRoutes(appRoutes)

  useEffect(() => {
    const initAuth = async () => {
      try {
        setLoading(true)
        await refresh()

        if (AUTH_ROUTES.includes(location.pathname)) {
          navigate('/', { replace: true })
        }
      } catch {
        if(!AUTH_ROUTES.includes(location.pathname)) {
          navigate('/login', {replace: true} )
        }
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [location.pathname, navigate])

  if (loading) {
    return <div>Carregando...</div>
  }

  return element
}

export default App
