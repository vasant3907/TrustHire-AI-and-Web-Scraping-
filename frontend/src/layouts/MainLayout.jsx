import React from 'react';
import { Navbar } from '../components/Navbar';

export const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="container mx-auto">
        {children}
      </main>
    </div>
  );
};

export default MainLayout;
