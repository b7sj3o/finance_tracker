import './styles/tailwind.css';
import { FC } from 'react'; // Alias for FunctionComponent
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
// import { NavBar } from './components';

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  return <RouterProvider router={router} />;
};

export default App;
