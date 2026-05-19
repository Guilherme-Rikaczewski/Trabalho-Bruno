import api from './api'

export const getRecentSheets = async () => {
  try{
    const response = await api.get('/sheets/recent')
    return response.data
  }catch(error){
    if (error.response?.status === 404) {
      return []
    }
    console.error(error || 'Erro ao encontrar fichas recentes!')
    throw error
  }
}
