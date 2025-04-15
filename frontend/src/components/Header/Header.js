import React from 'react';
import logo from './ressources/logo.svg'; // Ensure the path to your logo is correct
import './Header.css'; // Create a CSS file for styling

const Header = () => {
  return (
    <header className="header-container">
      <img src={logo} className="header-logo" alt="React Logo" />
      <h1 className="header-title">Data Forge Lab</h1>
    </header>
  );
};

export default Header;
