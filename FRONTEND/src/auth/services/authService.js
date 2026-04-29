import { authApi, setAccessToken } from '../../services/api'

export const login = async (email, password) => {
  const formData = new URLSearchParams()
  formData.set('username', email)
  formData.set('password', password)

  const response = await authApi.post('/auth/login/', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  const token = response.data.access_token
  setAccessToken(token)
  return token
}

export const refresh = async () => {
  try {
    const { data } = await authApi.post('/auth/refresh/')
    if (data) {
      setAccessToken(data.access_token)
      return data.access_token
    }
  } catch (error) {
    setAccessToken(null)
    console.warn('Usuário não logado ou refresh falhou: ', error)
    throw error
  }
}

export const logout = async () => {
  await authApi.post('/auth/logout/')
  setAccessToken(null)
}
