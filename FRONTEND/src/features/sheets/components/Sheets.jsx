import styles from './Sheets.module.scss'
import classNames from 'classnames/bind';

const cx = classNames.bind(styles)

export const Sheets = ({sheet, userType}) => {
  if(userType == 'player')
    console.log(userType) // não sei ainda
  if(userType == 'gameMaster')
    console.log(userType)

  return (
    <div className={cx('sheets-group', 'list-group')}>
      <a className={cx('sheets', 'list-group-item', 'mb-2')}>
        {sheet.name_sheet}
      </a>
    </div>
  )
}