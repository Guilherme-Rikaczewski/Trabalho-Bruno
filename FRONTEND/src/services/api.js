import axios from "axios"
import { refresh } from "../auth/services/authService"

let accessToken = null

let isRefreshing = false
let failedRequestQueue  = []
const apiBaseUrl = import.meta.env.VITE_API_URL ?? "/api"

const api = axios.create({
  baseURL: apiBaseUrl,
  withCredentials: true
})

export const authApi = axios.create({
  baseURL: apiBaseUrl,
  withCredentials: true
})

// antes da requisição
api.interceptors.request.use((config) => { 
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// depois da requisição
api.interceptors.response.use(
  (response) => response,
  async (erro) => {
    const originalRequest = erro.config
    const status = erro.response?.status

    if(status === 401 && originalRequest && !originalRequest._retry) {
      if(isRefreshing) {
        return new Promise((resolve, reject) => {
          failedRequestQueue.push({ resolve, reject })
        })
        .then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }).catch(err => Promise.reject(err))
      }
      originalRequest._retry = true
      isRefreshing = true

      try {
        const newToken = await refresh()
        api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
        setAccessToken(newToken)
        processQueue(null, newToken)
        return api(originalRequest)

      } catch (err) {
        setAccessToken(null)
        processQueue(err, null)
        return Promise.reject(err)

      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(erro)
  }
)

const processQueue = (erro, token = null) => {
   failedRequestQueue.forEach(promise => {
    if (erro) {
      promise.reject(erro)
    } else {
      promise.resolve(token)
    }
  })
  failedRequestQueue = []
}

export const setAccessToken = (token) => {
  accessToken = token
}

export const getAccessToken = () => accessToken

export default api
