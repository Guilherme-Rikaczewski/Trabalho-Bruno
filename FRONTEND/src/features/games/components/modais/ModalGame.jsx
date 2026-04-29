import cn from 'classnames/bind'
import s from './ModalGame.module.scss'
import Input from "@/shared/forms/Input"
import { useState, useEffect } from 'react'
import { Icon } from '../../../../shared/icones/Icon'
import { createGame, editGame, joinGame, deleteGame } from '../../../../services/gamesService'

export const ModalGame = ({ type, atualizaGames, dados }) => {
  const [formGame, setFormGame] = useState({ id: null, name: '' })
  const [formJoin, setFormJoin] = useState({ code: '' })

  const isNewGame = type == 1
  const isEditGame = type == 2
  const isJoinGame = type == 3
  const isDeleteGame = type == 4

  const id =
    isNewGame ? 'newGame' :
    isEditGame ? 'editGame' :
    isJoinGame ? 'joinGame' :
    isDeleteGame ? 'deleteGame' : ''

  useEffect(() => {
     if(isEditGame && dados) {
      setFormGame({
        id: dados.id,
        name: dados.room_name ?? dados.name ?? '',
      })
    }else {
      setFormGame({
        id: null,
        name: '',
      })
    }
  }, [dados, isEditGame])

  const handleDeleteClick = async () => {
    try {
      await deleteGame(formGame.id)
      atualizaGames?.({ id: formGame.id }, 'delete')
    } catch {
      alert('Erro ao remover a sala!')
    }
  }

  const handleChange = (name, value) => {
    if (isNewGame || isEditGame) {
      setFormGame({ ...formGame, [name]: value })
    }
    if (isJoinGame) {
      const nextValue = name === 'code'
        ? value.toUpperCase().replace(/\s/g, '').slice(0, 6)
        : value
      setFormJoin({ ...formJoin, [name]: nextValue })
    }
  }

  const handleSubmit = async () => {
    try {
      if (isNewGame || isEditGame) {
        const response = isNewGame
          ? await createGame(formGame.name)
          : await editGame(formGame.id, formGame.name)
        if (response) {
          atualizaGames?.(response, isEditGame ? 'edit' : '')
        }
      }
      if (isJoinGame) {
        const response = await joinGame(formJoin.code)
        if(response) {
          atualizaGames?.(response, '')
        }
      }
    } catch (error) {
      const detail = error.response?.data?.detail
      alert(detail ?? 'Não foi possível concluir a ação.')
    }
  }

  const getBody = () => {
    if (isNewGame || isEditGame) {
      return (
        <div className="modal-body container">
          <div className="row">
            <Input
              label="Room Name"
              placeholder="A room waiting for its story..."
              name="name"
              value={formGame.name}
              handleChange={handleChange}
              theme="ipt-second"
              hasIcon={true}
              nameIcon="feather"
              className="col"
            />
          </div>
        </div>
      )
    }

    if (isDeleteGame) {
      return (
        <div className="modal-body container">
          <div className="row">
            <h3>{dados?.room_name ?? dados?.name}</h3>
            <p className="text-center">
              This action will delete your room.
            </p>
            <p className="text-center">Are you sure?</p>
          </div>
        </div>
      )
    }

    if (isJoinGame) {
      return (
        <div className="modal-body">
          <Input
            label="Room Code"
            placeholder="Enter the 6-character code..."
            name="code"
            value={formJoin.code}
            handleChange={handleChange}
            theme="ipt-second"
            hasIcon={true}
            nameIcon="keyRound"
          />
        </div>
      )
    }
  }

  return (
    <div
      className="modal fade"
      id={id}
      tabIndex="-1"
      aria-labelledby={id + 'Label'}
      aria-hidden="true"
    >
      <div className={cn("modal-dialog modal-dialog-centered")}>
        <div className={cn("modal-content", s.modalGame)}>
          <div className="modal-header">
            <Icon name={(isNewGame || isEditGame) ? 'dices' : 'swords'} />
            <h1 className="modal-title fs-5 ps-2" id={id + 'Label'}>
              {isNewGame
                ? 'Create a New Room'
                : isJoinGame
                ? 'Join a Room'
                : 'Edit your Room'}
            </h1>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          {getBody()}

          <div className={cn("modal-footer", { 'justify-content-between': isEditGame })}>
            {isEditGame && (
              <button
                className={cn(s.deleteGame)}
                onClick={handleDeleteClick}
                data-bs-dismiss="modal"
              >
                <Icon name="trash2" />
              </button>
            )}
            <div className={cn("d-flex gap-2", s.divBotoes)}>
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">
                Back
              </button>
              <button
                type="button"
                className="btn btn-primary-green"
                onClick={handleSubmit}
                data-bs-dismiss="modal"
              >
                {isNewGame
                  ? 'Create Room'
                  : isJoinGame
                  ? 'Enter Room'
                  : 'Save Room'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
