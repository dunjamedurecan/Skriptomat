import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Feed from "./pages/Feed";
import Login from "./pages/Login";
import Registration from "./pages/Registration";
import ProtectedRoute from "./components/ProtectedRoute";
import UserProfile from "./pages/UserProfile";
import ViewProfile from "./pages/ViewProfile";

export default function App(){
  return(
    <div className="app">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/about" element={<About/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/registration" element={<Registration/>}/>
        <Route path="/my-profile" element={<UserProfile/>}/>
        <Route path="/profile/:username" element={<ViewProfile/>}/>
        <Route
          path="/feed"
          element={
            <ProtectedRoute>
              <Feed/>
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
}