import api from "./api"

const normalizeRoom = (room) => {
  if (!room) {
    return null
  }

  return {
    ...room,
    name: room.room_name ?? room.name ?? "",
    room_name: room.room_name ?? room.name ?? "",
    imagePath: room.imagePath ?? null,
  }
}

export const getRecentGames = async () => {
  try{
    const response = await api.get('/rooms/recent/')
    return Array.isArray(response.data)
      ? response.data.map(normalizeRoom)
      : []
  }catch(error) {
    console.warn(error || 'Erro ao carregar as salas!')
    throw error
  }
}

export const createGame = async (name) => {
  try{
    const response = await api.post('/rooms/', { room_name: name })
    return normalizeRoom(response.data)
  }catch (error) {
    console.error(error || 'Erro ao criar a sala!')
    throw error
  }
}

export const editGame = async (id, name) => {
  try{
    const response = await api.patch(`/rooms/${id}`, { room_name: name })
    return normalizeRoom(response.data)
  }catch (error) {
    console.error(error || 'Erro ao editar a sala!')
    throw error
  }
}

export const joinGame = async (code) => {
  try{
    const response = await api.post(`/rooms/join/${code.trim().toUpperCase()}`)
    return normalizeRoom(response.data)
  }catch (error) {
    console.error(error || 'Erro ao entrar na sala!')
    throw error
  }
}

export const deleteGame = async (id) => {
  try{
    await api.delete(`/rooms/${id}`)
  }catch (error) {
    console.error(error || 'Erro ao remover a sala!')
    throw error
  }
}
