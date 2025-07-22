import './App.css';

import { ThemeProvider } from '@mui/material';
import DefaultTheme from './view/themes/DefaultTheme';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Helmet } from 'react-helmet';

import { Footer } from './view/components/footer/Footer';
import { Header } from './view/components/header/Header';
import { Splash } from './view/pages/splash/Splash';
import { Login } from './view/pages/login/Login';
import { Signup } from './view/pages/signup/Signup';
import { Home } from './view/pages/home';
import { ViewRooms } from './view/pages/viewRooms/ViewRooms';
import { BookingHistory } from './view/pages/bookingHistory/BookingHistory';
import { CreateBooking } from './view/pages/createBooking/CreateBooking';
import { CancelBooking } from './view/pages/cancelBooking/CancelBooking';
import { Dashboard } from './view/pages/dashboard/Dashboard';
import { ViewBuildings } from './view/pages/viewBuildings/ViewBuildings';
import { EditAccount } from './view/pages/editAccount/EditAccount';

import { AuthProvider } from './wrappers/AuthContext'
import { ProtectedRoutes } from './wrappers/ProtectedRoutes'

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

        <AuthProvider>
          <Header />
          <Routes>
            <Route path="/" element={<Splash />} />
            <Route path="signup" element={<Signup />} />
            <Route path="login" element={<Login />} />
            <Route path="home" element={<ProtectedRoutes><Home /></ProtectedRoutes>} />
            <Route path="viewBookings" element={<ProtectedRoutes><ViewRooms/></ProtectedRoutes>} />
            <Route path="editRooms/:buildingID" element={<ProtectedRoutes><ViewRooms mode="edit"/></ProtectedRoutes>} />
            <Route path="deleteRooms/:buildingID" element={<ProtectedRoutes><ViewRooms mode="delete"/></ProtectedRoutes>} />
            <Route path="bookRoom" element={<ProtectedRoutes><CreateBooking /></ProtectedRoutes>} />
            <Route path="cancelBooking" element={<ProtectedRoutes><CancelBooking /></ProtectedRoutes>} />
            <Route path="bookingHistory" element={<ProtectedRoutes><BookingHistory/></ProtectedRoutes>} />
            <Route path="dashboard" element={<ProtectedRoutes><Dashboard /></ProtectedRoutes>} />
            <Route path="manageFacilities" element={<ProtectedRoutes><ViewBuildings /></ProtectedRoutes>} />
            <Route path="editAccount" element={<ProtectedRoutes><EditAccount/></ProtectedRoutes>} />
          </Routes>
          <Footer />
        </AuthProvider>

      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
