import './Redirection.module.scss'
import styles from './Redirection.module.scss'
import { useNavigate } from 'react-router-dom'

const Redirection = ({
  text,
  route
}) => {
    const navigate = useNavigate()
    const func = () => {
      navigate(`/${route}`, {replace: true} )
    }
  return (
    <strong className={styles.p} onClick={func} style={{ cursor: 'pointer' }}>
      {text}
    </strong>
  )
}

export default Redirection
