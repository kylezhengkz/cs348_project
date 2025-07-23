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
import { ViewBooking } from './view/pages/viewBooking/ViewBooking';
import { BookingHistory } from './view/pages/bookingHistory/BookingHistory';
import { CancelBooking } from './view/pages/cancelBooking/CancelBooking';
import { Dashboard } from './view/pages/dashboard/Dashboard';
import { ManageRooms } from './view/pages/manageRooms/ManageRooms';
import { ManageBuildings } from './view/pages/manageBuildings/ManageBuildings';
import { EditAccount } from './view/pages/editAccount/EditAccount';
import { AccessDenied } from './view/pages/accessDenied/AccessDenied';
import { RouteTracker } from './view/components/routeTracker/RouteTracker';


import { AuthProvider } from './wrappers/AuthContext'
import { ProtectedRoutes } from './wrappers/ProtectedRoutes'
import { PublicRoutes } from './wrappers/PublicRoutes';
import { AdminProtectedRoutes } from './wrappers/AdminProtectedRoutes';


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
          <RouteTracker />
          <Routes>
            <Route path="/" element={<PublicRoutes><Splash /></PublicRoutes>} />
            <Route path="signup" element={<PublicRoutes><Signup /></PublicRoutes>} />
            <Route path="login" element={<PublicRoutes><Login /></PublicRoutes>} />
            <Route path="home" element={<ProtectedRoutes><Home /></ProtectedRoutes>} />
            <Route path="viewBooking" element={<ProtectedRoutes><ViewBooking/></ProtectedRoutes>} />
            <Route path="cancelBooking" element={<ProtectedRoutes><CancelBooking /></ProtectedRoutes>} />
            <Route path="bookingHistory" element={<ProtectedRoutes><BookingHistory/></ProtectedRoutes>} />
            <Route path="manageRooms" element={<AdminProtectedRoutes><ManageRooms /></AdminProtectedRoutes>} />
            <Route path="manageBuildings" element={<AdminProtectedRoutes><ManageBuildings /></AdminProtectedRoutes>} />
            <Route path="accessDenied" element={<AccessDenied />} />
            <Route path="editAccount" element={<ProtectedRoutes><EditAccount/></ProtectedRoutes>} />
          </Routes>
          <Footer />
        </AuthProvider>

      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
