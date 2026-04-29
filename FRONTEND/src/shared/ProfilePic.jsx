import { useEffect, useState } from "react"
import cn from "classnames/bind"
import { Icon } from "./icones/Icon"
import s from './ProfilePic.module.scss'
import { getUser } from "../services/usersService"

const getInitials = (username = "") => {
  return username
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("")
}

export const ProfilePic = ({ justIcon = false, size = '40px' }) => {
  const [username, setUsername] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      if(!justIcon) {
        try {
          const user = await getUser()
          setUsername(user.username ?? '')
        } catch {
          setUsername('')
        }
      }
    }

    fetchData()
  }, [justIcon])

  const initials = getInitials(username)

  const getComponent = () => {
    return (
      <div
        className={cn(s.userBox, 'me-2')}
        style={{height: size, width: size, minHeight: size, minWidth: size }}
      >
        {(!justIcon && initials) ? (
          <span>{initials}</span>
        ) : (
          <Icon name='user' size='25' />
        )}
      </div>
    )
  }

  return (
    <>
      { justIcon ? getComponent() : 
      <a className={cn("navbar-brand", "menu-user-decor", s.userArea)} href="#">
        { getComponent() }
        { username }
        <Icon name='chevronDown' />
      </a> }
    </>
  )
}
