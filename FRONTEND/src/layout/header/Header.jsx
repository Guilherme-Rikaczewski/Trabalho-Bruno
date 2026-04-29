import { ProfilePic } from '../../shared/ProfilePic';
import './Header.scss';
import { NavLink } from 'react-router-dom';

const Header = () => {

  const expand = () => {
    let menu = document.getElementById("mb-nav")
    menu.classList.toggle("expanded")
  }

  return (
    <header className='header-layout shadow'>
      <nav className="navbar-expand-lg bg-gray py-2 mb-height">
        <div className="container">
          <div className="row">
            <div className="col-2">
              <div className="logo-box">
                <img
                  src="Logotipo_Dice_Tales.png" // logo à fazer
                  alt="Logo - Dado em chamas em um livro aberto"
                  style={{ height: "3rem" }}
                /> 
                <img
                  src="logo_fonte.png"
                  alt="Logo - Dice Tales"
                  style={{ height: "2.4rem" }}
                  className='logo-fonte d-none d-lg-block'
                />
              </div>
            </div>
            <div className="col-8 menu-box">
              <div
                className="collapse navbar-collapse"
                id="navbarSupportedContent"
              >
                <ul className="navbar-nav me-auto mb-2 mb-lg-0 menu-items container">
                  <li className="nav-item">
                    <NavLink
                      className={({ isActive }) =>
                        `nav-link animated-title menu-txt-decor 
                        ${isActive ? "active-item" : ""}`
                      }
                      aria-current="page"
                      to="/"
                    >
                      Home
                    </NavLink>
                  </li>
                  <li className="nav-item">
                    <NavLink
                      className={({ isActive }) =>
                        `nav-link animated-title menu-txt-decor 
                        ${isActive ? "active-item" : ""}`
                      }
                      aria-current="page"
                      to="/teste"
                    >
                      Games
                    </NavLink>
                  </li>
                  <li className="nav-item">
                    <NavLink
                      className={({ isActive }) =>
                        `nav-link animated-title menu-txt-decor 
                        ${isActive ? "active-item" : ""}`
                      }
                      aria-current="page"
                      to="/sheets"
                    >
                      Sheets
                    </NavLink>
                  </li>
                  <li className="nav-item">
                    <NavLink
                      className={({ isActive }) =>
                        `nav-link animated-title menu-txt-decor 
                        ${isActive ? "active-item" : ""}`
                      }
                      aria-current="page"
                      to="/community"
                    >
                      Community
                    </NavLink>
                  </li>
                </ul>
              </div>
            </div>
            <div className="col-2 d-flex justify-content-center">
              <ProfilePic />
              <div className="mb-menu" onClick={expand}>
                <div className="menu-icon"></div>
                <div className="menu-icon"></div>
                <div className="menu-icon"></div>
              </div>
            </div>
          </div>
        </div>
      </nav>
      <div className="expanded-menu" id="mb-nav">
        <div className="menu-mb-text bg-gray atual">Home</div>
        <div className="menu-mb-text bg-gray">Games</div>
        <div className="menu-mb-text bg-gray">Sheets</div>
        <div className="menu-mb-text bg-gray">Community</div>
      </div>
    </header>
  );
}

export default Header;
