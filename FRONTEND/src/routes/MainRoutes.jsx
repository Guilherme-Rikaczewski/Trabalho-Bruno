import Layout from "../layout/Layout";
import Home from "../features/home/pages/Home";
import Teste from "../features/home/Teste";
import SheetsPage from "../features/sheets/pages/SheetsPage";

const mainRoutes = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'sheets', element: <SheetsPage /> },
      { path: 'teste', element: <Teste /> },
    ]
  }
]

export default mainRoutes
