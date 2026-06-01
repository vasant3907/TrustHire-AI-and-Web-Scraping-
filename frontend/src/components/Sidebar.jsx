import React from 'react';

export const Sidebar = ({ isOpen }) => {
  return (
    <aside className={`${isOpen ? 'w-64' : 'w-0'} bg-gray-800 text-white transition-all duration-300 overflow-hidden`}>
      <nav className="p-4 space-y-4">
        <a href="/dashboard" className="block hover:bg-gray-700 p-2 rounded">Dashboard</a>
        <a href="/analyze" className="block hover:bg-gray-700 p-2 rounded">Analyze Job</a>
        <a href="/reports" className="block hover:bg-gray-700 p-2 rounded">Reports</a>
        <a href="/profile" className="block hover:bg-gray-700 p-2 rounded">Profile</a>
      </nav>
    </aside>
  );
};

export default Sidebar;
