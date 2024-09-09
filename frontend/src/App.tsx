import './styles/tailwind.css';
import './App.css';

import { FC, useEffect } from 'react'; // Alias for FunctionComponent
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { NavBar } from './components';

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  
  useEffect(() => {
    const tg = window.Telegram.WebApp;

    // fullscreen set telegram app
    tg.expand();

    // telegram theme options
    document.body.style.backgroundColor = tg.themeParams.bg_color || '#ffffff';
    document.body.style.color = tg.themeParams.text_color || '#000000';

    console.log(tg.initDataUnsafe.user);

    // mainButton
    tg.MainButton.setText('Підтвердити');
    tg.MainButton.onClick(() => {
      tg.close();
    });
    tg.MainButton.show();
  }, []);



  return (<>
  <RouterProvider router={router} />
  <NavBar />
  </>
  )
};

export default App;
