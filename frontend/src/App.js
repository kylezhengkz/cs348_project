import './App.css';

import { ThemeProvider } from '@mui/material';
import DefaultTheme from './view/themes/DefaultTheme';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Helmet } from 'react-helmet';

import { Footer } from './view/components/footer/Footer';
import { Header } from './view/components/header/Header';
import { Home } from './view/pages/home';
import { ViewBooking } from './view/pages/viewBooking/ViewBooking';
import { CreateBooking } from './view/pages/createBooking/CreateBooking';
import { CancelBooking } from './view/pages/cancelBooking/CancelBooking';


function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={DefaultTheme}>
        <Helmet>
          <title>Room Booking App</title>

          <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
          <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" crossorigin="anonymous"></link>

          <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" type="text/css"
                integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous" />
        </Helmet>

        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="viewBooking" element={<ViewBooking />} />
          <Route path="bookRoom" element={<CreateBooking />} />
          <Route path="cancelBooking" element={<CancelBooking />} />
        </Routes>

        <Footer />
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
