/* import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import { AuthProvider } from "./context/AuthContext"

function App() {
  return(
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} /> 
          <Route path="/dashboard" element={<Dashboard />} /> 
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App */
import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import { api } from "./api/api";
import GiveKudoForm from "./components/GiveKudoForm";
import ReceivedKudos from "./components/ReceivedKudos"

export default function App() {
  const [user, setUser] = useState(() =>{
    try {
      return JSON.parse(localStorage.getItem('user'));
    } catch {
      return null;
    }
  });

  const [remaining, setRemaining] = useState(3)
  const[refreshCounter, setRefreshCounter] = useState(0)

  useEffect(() => {
    if(user) {
      api.remainingKudos(user.id).then((data) => setRemaining(data.remaining_kudos)).catch(() => setRemaining(3))
    }
  }, [user])

  const handleLogin = (userObj) =>{
    setUser(userObj)
    localStorage.setItem('user', JSON.stringify(userObj))
  };

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('user')
  };

  if(!user){
    return <Login onLogin={handleLogin} />
  }

 try{
  return (
    <div style={{ padding:'2rem' }}>
      <header style={{ display: 'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'2rem' }}>
        <div >
          <h2>Kudos App</h2>
          <p>
            Logged in as <strong>{user.username}</strong> ({user.organization})
          </p>
        </div>
        <div>
          <p>
            Remaining Kudos: {remaining}
          </p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <main>
        <p>Welcome {user.username}. Let's spread some kudos</p>
        <GiveKudoForm user={user} onKudoGiven={() => {
          api.remainingKudos(user.id).then((data) => setRemaining(data.remaining_kudos || 3)).catch(() => setRemaining(3))

          setRefreshCounter(prev => prev+1)
        }} />

        <ReceivedKudos userId={user.id} refreshCounter={refreshCounter} />
      </main>
    </div>
  );}
  catch(err) {
    console.error("Render failed:", err);
    return<div>Render Failed</div>
  }
}