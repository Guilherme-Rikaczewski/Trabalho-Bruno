import Input from "@/shared/forms/Input"
import styles from "./Login.module.scss"
import login_art from "@/assets/login_art.png"
import { useState } from "react"
import { ProfilePic } from "@/shared/ProfilePic"
import { login } from "../services/authService"
import Redirection from "../components/Redirection"
import { useNavigate } from "react-router-dom"

const Login = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })

  const handleChange = (name, value) => {
    setForm({ ...form, [name]: value })
  }

  const handleSubmit = async () => {
    try{
      const token = await login(form.email, form.password)
      if(token) {
        navigate('/')
      }
    }catch {
      alert('Dados inválidos!')
    }
  }

  return (
    <main className={styles.main}>
      <div className={styles.box}>

        <div className={styles.leftSide}>
          <img src={login_art} alt="Login Art" className={styles.loginArt} />
        </div>
        <div className={styles.rightSide}>
          <div className={styles.iconContainer}>
            <ProfilePic justIcon={true} size='50px'/>
          </div>
          <h1 className={styles.h1}>LOGIN</h1>
          <form className={styles.form} >
            <Input
              label="Email"
              placeholder="What is your email?"
              name='email'
              value={form.email}
              handleChange={handleChange}
              margin={0}
            />
            
            <Input
              label="Password"
              type="password"
              placeholder="Is it really you?"
              name='password'
              value={form.password}
              handleChange={handleChange}
              margin={10}
            />

            <div className={styles.forgot}>
              <a className={styles.a} href="#">Forgot Password?</a>
            </div>

            <button type="button" onClick={handleSubmit}
            className={styles.loginButton}>Login</button>

            <b className={styles.divider}>OR</b>

            <p className={styles.p}>
              Create a <Redirection text='new account' route='register' />
            </p>
          </form>
        </div>
      </div>
    </main>
  )
}

export default Login;
