import { useState } from "react"
import cn from "classnames/bind"
import Input from "@/shared/forms/Input"
import { SelectOption } from "@/shared/forms/SelectOption"
import { Icon } from "@/shared/icones/Icon"
import { createAiSheet } from "@/services/aiService"
import s from "./AiSheetModal.module.scss"

const cx = cn.bind(s)

const initialFormState = {
  game: "D&D 5e",
  name: "",
  race: "",
  char_class: "",
  origin: "",
  weapon: "",
  god: "",
  build: "",
}

const gameOptions = [{ id: 1, descricao: "D&D 5e" }]

const classOptions = [
  "Barbarian",
  "Bard",
  "Cleric",
  "Druid",
  "Fighter",
  "Monk",
  "Paladin",
  "Ranger",
  "Rogue",
  "Sorcerer",
  "Warlock",
  "Wizard",
  "Artificer",
].map((descricao) => ({
  id: descricao,
  descricao,
}))

const raceOptions = [...new Set([
  "Aasimar",
  "Dragonborn",
  "Dwarf",
  "Elf",
  "Gnome",
  "Goliath",
  "Halfling",
  "Human",
  "Orc",
  "Tiefling",
  "Dhampir",
  "Boggart",
  "Faerie",
  "Flamekin",
  "Kithkin",
  "Lorwyn Changeling",
  "Lorwyn-Shadowmoor Elf",
  "Rimekin",
  "Aarakocra",
  "Air Genasi",
  "Bugbear",
  "Centaur",
  "Changeling",
  "Deep Gnome",
  "Duergar",
  "Earth Genasi",
  "Eladrin",
  "Fairy",
  "Firbolg",
  "Fire Genasi",
  "Githyanki",
  "Githzerai",
  "Goblin",
  "Haregon",
  "Hobgoblin",
  "Kenku",
  "Kobold",
  "Lizardfolk",
  "Minotaur",
  "Satyr",
  "Sea Elf",
  "Shadar-kai",
  "Shifter",
  "Tabaxi",
  "Tortle",
  "Triton",
  "Water Genasi",
  "Yuan-ti",
])]
  .sort((a, b) => a.localeCompare(b))
  .map((descricao) => ({
    id: descricao,
    descricao,
  }))

export const AiSheetModal = () => {
  const [formData, setFormData] = useState(initialFormState)
  const [generatedSheet, setGeneratedSheet] = useState(null)
  const [errorMessage, setErrorMessage] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (name, value) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true)
      setErrorMessage("")

      const response = await createAiSheet(formData)
      setGeneratedSheet(response)
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail ?? "It was not possible to generate the sheet using AI."
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleReset = () => {
    setFormData(initialFormState)
    setGeneratedSheet(null)
    setErrorMessage("")
    setIsSubmitting(false)
  }

  return (
    <div
      className="modal fade"
      id="createAiSheetModal"
      tabIndex="-1"
      aria-labelledby="createAiSheetModalLabel"
      aria-hidden="true"
    >
      <div className="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
        <div className={cx("modal-content", s.modalSheet)}>
          <div className={cx("modal-header", s.modalHeader)}>
            <div className={cx("d-flex", "align-items-center", "gap-2")}>
              <Icon name="penTool" />
              <h1 className={cx("modal-title", "fs-5", s.modalTitle)} id="createAiSheetModalLabel">
                Create Sheet With AI
              </h1>
            </div>
            <button
              type="button"
              className={cx("btn-close", s.closeButton)}
              data-bs-dismiss="modal"
              aria-label="Close"
              onClick={handleReset}
            ></button>
          </div>

          <div className={cx("modal-body", s.modalBody)}>
            <div className={cx("container-fluid")}>
              <div className={cx("row", "g-3")}>
                <SelectOption
                  label="Game"
                  name="game"
                  value={formData.game}
                  handleChange={handleChange}
                  listaOpcoes={gameOptions}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-4"
                />

                <Input
                  label="Name"
                  placeholder="Who is your character?"
                  name="name"
                  value={formData.name}
                  handleChange={handleChange}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-8"
                />

                <SelectOption
                  label="Race"
                  name="race"
                  value={formData.race}
                  handleChange={handleChange}
                  listaOpcoes={raceOptions}
                  descricaoPadrao="Choose a race..."
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />

                <SelectOption
                  label="Class"
                  name="char_class"
                  value={formData.char_class}
                  handleChange={handleChange}
                  listaOpcoes={classOptions}
                  descricaoPadrao="Choose a class..."
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />

                <Input
                  label="Origin"
                  placeholder="Where did this character come from?"
                  name="origin"
                  value={formData.origin}
                  handleChange={handleChange}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />

                <Input
                  label="Favorite Weapon"
                  placeholder="What do they love to wield?"
                  name="weapon"
                  value={formData.weapon}
                  handleChange={handleChange}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />

                <Input
                  label="Divinity"
                  placeholder="Which deity do they follow?"
                  name="god"
                  value={formData.god}
                  handleChange={handleChange}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />

                <Input
                  label="Build"
                  placeholder="Subclass, attributes, armored, anything..."
                  name="build"
                  value={formData.build}
                  handleChange={handleChange}
                  theme="ipt-second"
                  labelClassName={s.sheetLabel}
                  className="col-12 col-lg-6"
                />
              </div>

              {errorMessage && (
                <div className={cx("mt-4", s.errorBox)}>
                  {errorMessage}
                </div>
              )}

              {generatedSheet && (
                <section className={cx("mt-4", s.generatedSheet)}>
                  <header className={cx(s.generatedHeader)}>
                    <div>
                      <span className={cx(s.generatedEyebrow)}>Generated with AI</span>
                      <h2 className={cx(s.generatedName)}>{generatedSheet.name}</h2>
                    </div>
                    <div className={cx(s.generatedTags)}>
                      <span>{generatedSheet.game}</span>
                      <span>{generatedSheet.race}</span>
                      <span>{generatedSheet.char_class}</span>
                    </div>
                  </header>

                  <div className={cx("row", "g-3", s.summaryGrid)}>
                    <div className="col-12 col-md-6 col-xl-3">
                      <div className={cx(s.summaryCard)}>
                        <strong>Origin</strong>
                        <span>{generatedSheet.origin || "Not specified"}</span>
                      </div>
                    </div>
                    <div className="col-12 col-md-6 col-xl-3">
                      <div className={cx(s.summaryCard)}>
                        <strong>Weapon</strong>
                        <span>{generatedSheet.weapon || "Not specified"}</span>
                      </div>
                    </div>
                    <div className="col-12 col-md-6 col-xl-3">
                      <div className={cx(s.summaryCard)}>
                        <strong>Divinity</strong>
                        <span>{generatedSheet.god || "Not specified"}</span>
                      </div>
                    </div>
                    <div className="col-12 col-md-6 col-xl-3">
                      <div className={cx(s.summaryCard)}>
                        <strong>Build</strong>
                        <span>{generatedSheet.build || "Not specified"}</span>
                      </div>
                    </div>
                  </div>

                  <div className={cx("row", "g-3")}>
                    <div className="col-12">
                      <article className={cx(s.detailCard)}>
                        <h3>Lore</h3>
                        <p>{generatedSheet.lore}</p>
                      </article>
                    </div>
                    <div className="col-12 col-xl-6">
                      <article className={cx(s.detailCard)}>
                        <h3>Physical Characteristics</h3>
                        <p>{generatedSheet.physical_characteristics}</p>
                      </article>
                    </div>
                    <div className="col-12 col-xl-6">
                      <article className={cx(s.detailCard)}>
                        <h3>Personality Traits</h3>
                        <p>{generatedSheet.personality_traits}</p>
                      </article>
                    </div>
                    <div className="col-12">
                      <article className={cx(s.detailCard)}>
                        <h3>Other Characteristics</h3>
                        <p>{generatedSheet.other_characteristics}</p>
                      </article>
                    </div>
                  </div>
                </section>
              )}
            </div>
          </div>

          <div className={cx("modal-footer", s.modalFooter)}>
            <button
              type="button"
              className="btn btn-secondary"
              data-bs-dismiss="modal"
              onClick={handleReset}
            >
              Close
            </button>
            <button
              type="button"
              className={cx("btn", "btn-primary-green", s.generateButton)}
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Creating..." : "Create Sheet With AI"}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
