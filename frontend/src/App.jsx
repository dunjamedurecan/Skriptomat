import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Feed from "./pages/Feed";
import Login from "./pages/Login";
import Registration from "./pages/Registration";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App(){
  return(
    <div className="app">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/about" element={<About/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/registration" element={<Registration/>}/>
        
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