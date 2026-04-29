import { Icon } from '../icones/Icon'
import s from './Inputs.module.scss'
import cn from 'classnames'

export const SelectOption = ({
  label = '',
  name,
  value,
  handleChange,
  listaOpcoes = [],
  descricaoPadrao,
  theme = 'ipt-primary',
  className,
  labelClassName
}) => {
  const id = `${label.replace(/\s+/g, '')}Select`

  return (
    <div className={cn('form-group', className)}>
      <label htmlFor={id} className={cn(s.label, labelClassName)}>{label}</label>
      <div className={cn(s.input, theme)}>
        <select className='form-control'
          id={id}
          name={name}
          value={value ?? ''}
          onChange={(e) => handleChange?.(e.target.name, e.target.value)}>
          {descricaoPadrao && (
            <option value=''>{descricaoPadrao}</option>
          )}
          { listaOpcoes.map((item) => (
            <option
              key={item.id ?? item.value ?? item.descricao}
              value={item.value ?? item.descricao}>
              {item.descricao}
            </option>
          ))}
        </select>
        <Icon name='chevronDown' />
      </div>
    </div>
  )
}
