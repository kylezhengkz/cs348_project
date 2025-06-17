import './App.css';
import { ThemeProvider } from '@mui/material';
import DefaultTheme from './view/components/themes/DefaultTheme';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { Footer } from './view/components/footer/Footer';
import { Header } from './view/components/header/Header';
import { Home } from './view/pages/home';
import { ViewBooking } from './view/pages/viewBooking/ViewBooking';


function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={DefaultTheme}>
        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="viewBooking" element={<ViewBooking />} />
        </Routes>

        <Footer />
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
