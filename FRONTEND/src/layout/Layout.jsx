import { Outlet } from "react-router-dom";
import Footer from "./footer/Footer";
import Header from "./header/Header"

const Layout = () => {

  return (
    <>
      <Header />
      <main className="mt-5 pt-0 pt-md-2">
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default Layout;
