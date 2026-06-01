import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (!storedUser) {
      return null;
    }

    try {
      return JSON.parse(storedUser);
    } catch {
      localStorage.removeItem('user');
      localStorage.removeItem('access_token');
      return null;
    }
  });
  const [token, setToken] = useState(() => localStorage.getItem('access_token') || sessionStorage.getItem('access_token'));
  const loading = false;

  const login = (userData, accessToken, remember = true) => {
    const activeStorage = remember ? localStorage : sessionStorage;
    const inactiveStorage = remember ? sessionStorage : localStorage;
    inactiveStorage.removeItem('access_token');
    inactiveStorage.removeItem('user');
    activeStorage.setItem('access_token', accessToken);
    activeStorage.setItem('user', JSON.stringify(userData));
    setToken(accessToken);
    setUser(userData);
  };

  const updateSession = (userData, accessToken = token) => {
    const activeStorage = localStorage.getItem('access_token') ? localStorage : sessionStorage;
    if (accessToken) {
      activeStorage.setItem('access_token', accessToken);
      setToken(accessToken);
    }
    activeStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, updateSession, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
