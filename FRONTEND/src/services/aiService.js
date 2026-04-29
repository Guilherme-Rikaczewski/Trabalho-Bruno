import api from "./api"

export const createAiSheet = async (attributes) => {
  try {
    const response = await api.post('/ai/create/', attributes)
    return response.data
  } catch (error) {
    console.error(error || 'Erro ao gerar ficha com IA!')
    throw error
  }
}
