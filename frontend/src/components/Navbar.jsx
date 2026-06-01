import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

export const Navbar = () => {
  const { user } = useContext(AuthContext);
  const isAdmin = Boolean(user?.is_admin);
  const links = isAdmin
    ? [
        ['Admin', '/admin'],
        ['Community', '/community'],
        ['Profile', '/profile'],
      ]
    : [
        ['Dashboard', '/dashboard'],
        ['Analyze Job', '/analyze'],
        ['Reports', '/reports'],
        ['Community', '/community'],
        ['Profile', '/profile'],
      ];

  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">TrustHire AI</h1>
        <div className="space-x-4">
          {links.map(([label, href]) => (
            <a key={href} href={href} className="hover:text-blue-200">{label}</a>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
