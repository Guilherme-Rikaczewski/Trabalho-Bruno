import cn from 'classnames'
import s from './Inputs.module.scss'
import { Icon } from '../icones/Icon'

const Input = ({
  label, 
  placeholder,
  type = 'text', 
  name,
  value,
  handleChange,
  margin,
  theme = 'ipt-primary',
  className,
  labelClassName,
  hasIcon = false,
  nameIcon
}) => {

  return (
    <div className={cn(s.div, className)}>
        <label style={{marginTop: margin}} className={cn(s.label, labelClassName)}> {label} 
          <div className={cn(s.input, 'd-flex flex-row', theme)}>
            <input type={type} 
              placeholder={placeholder} 
              name={name} 
              value={value ?? ''} 
              onChange={(e) => handleChange(e.target.name, e.target.value)} 
            />
            { hasIcon && <Icon name={nameIcon} className={s.icon} /> }
          </div>
        </label>
    </div>
  )
}

export default Input
