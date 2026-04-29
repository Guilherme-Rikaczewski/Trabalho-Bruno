import cn from "classnames/bind"
import { AiSheetModal } from "../components/AiSheetModal"
import s from "./SheetsPage.module.scss"

const cx = cn.bind(s)

const SheetsPage = () => {
  return (
    <main className={cx("container", s.sheetsPage)}>
      <section className={cx(s.actionArea)}>
        <button
          type="button"
          className={cx("btn", "btn-primary-green", "shadow", s.createButton)}
          data-bs-toggle="modal"
          data-bs-target="#createAiSheetModal"
        >
          Create sheet with AI
        </button>
      </section>

      <AiSheetModal />
    </main>
  )
}

export default SheetsPage
