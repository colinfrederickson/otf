import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Login from './components/login';
import Dashboard from './components/dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check for authentication token on component mount
  useEffect(() => {
    const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  const handleLogout = () => {
    // Clear tokens and update authentication state
    localStorage.removeItem('authToken');
    sessionStorage.removeItem('authToken');
    setIsAuthenticated(false);
  };

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <Routes>
        {/* Route for Login */}
        <Route 
          path="/" 
          element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Login onLoginSuccess={handleLoginSuccess} />} 
        />

        {/* Route for Dashboard */}
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Login onLoginSuccess={handleLoginSuccess} />} 
        />
        
        {/* Add additional routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;