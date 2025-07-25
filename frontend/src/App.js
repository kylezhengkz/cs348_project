import './App.css';

import { ThemeProvider } from '@mui/material';
import DefaultTheme from './view/themes/DefaultTheme';
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
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
import { ViewAdminLog } from './view/pages/viewAdminLog/ViewAdminLog';
import { AdminPage } from './view/pages/adminPage/AdminPage';
import { AccessDenied } from './view/pages/accessDenied/AccessDenied';
import { RouteTracker } from './view/components/routeTracker/RouteTracker';

import { AuthProvider } from './wrappers/AuthContext'
import { ProtectedRoutes } from './wrappers/ProtectedRoutes'
import { PublicRoutes } from './wrappers/PublicRoutes';
import { AdminProtectedRoutes } from './wrappers/AdminProtectedRoutes';

function App(){
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

function AppContent() {
  const hiddenHeaderFooterRoutes = ['/'];

  const location = useLocation();
  const hideHeaderFooter = hiddenHeaderFooterRoutes.includes(location.pathname);

  return (
    <ThemeProvider theme={DefaultTheme}>
      <Helmet>
        <title>Room Booking App</title>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" crossorigin="anonymous"></link>

        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" type="text/css"
              integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;500;700&display=swap" rel="stylesheet"></link>
        <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet" />
      </Helmet>

      <AuthProvider>
        {!hideHeaderFooter && <Header />}
        <RouteTracker />
        <Routes>
          <Route path="/" element={<PublicRoutes><Splash /></PublicRoutes>} />
          <Route path="signup" element={<PublicRoutes><Signup /></PublicRoutes>} />
          <Route path="login" element={<PublicRoutes><Login /></PublicRoutes>} />
          <Route path="home" element={<ProtectedRoutes><Home /></ProtectedRoutes>} />
          <Route path="viewBooking" element={<ProtectedRoutes><ViewBooking/></ProtectedRoutes>} />
          <Route path="cancelBooking" element={<ProtectedRoutes><CancelBooking /></ProtectedRoutes>} />
          <Route path="bookingHistory" element={<ProtectedRoutes><BookingHistory/></ProtectedRoutes>} />
          
          <Route path="adminPage" element={<AdminProtectedRoutes><AdminPage /></AdminProtectedRoutes>} />
          <Route path="manageRooms" element={<AdminProtectedRoutes><ManageRooms /></AdminProtectedRoutes>} />
          <Route path="manageBuildings" element={<AdminProtectedRoutes><ManageBuildings /></AdminProtectedRoutes>} />
          <Route path="viewAdminLog" element={<AdminProtectedRoutes><ViewAdminLog /></AdminProtectedRoutes>} />
          
          <Route path="accessDenied" element={<AccessDenied />} />
          <Route path="editAccount" element={<ProtectedRoutes><EditAccount/></ProtectedRoutes>} />
        </Routes>
        {!hideHeaderFooter && <Footer />}
      </AuthProvider>

    </ThemeProvider>
  );
}

export default App;
