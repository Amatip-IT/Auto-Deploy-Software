import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
    const navigate = useNavigate();
    const isLoggedIn = !!localStorage.getItem('authToken'); // Check if user is logged in

    const handleLogout = () => {
        // Clear authentication data
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        navigate('/'); // Redirect to login page
    };

    return (
        <header className="bg-blue-600 text-white py-4">
            <div className="container mx-auto flex justify-between items-center">
                {/* Brand/Logo */}
                <div className="flex items-center space-x-2">
                    <img
                        src="/path-to-logo.png" // Replace with your logo image path
                        alt="Amatip Logo"
                        className="w-8 h-8"
                    />
                    <Link
                        to={isLoggedIn ? "/dashboard" : "/"}
                        className="text-2xl font-bold hover:underline"
                    >
                        Amatip
                    </Link>
                </div>

                {/* Navigation Links */}
                {isLoggedIn && (
                    <nav className="hidden md:flex space-x-6">
                        <Link to="/dashboard" className="hover:underline">
                            Dashboard
                        </Link>
                        <Link to="/deployment/new" className="hover:underline">
                            New Deployment
                        </Link>
                        <Link to="/analytics" className="hover:underline">
                            Analytics
                        </Link>
                        <Link to="/wizard/step1" className="hover:underline">
                            Wizard Guide
                        </Link>
                    </nav>
                )}

                {/* Mobile Menu Placeholder */}
                {isLoggedIn && (
                    <div className="md:hidden">
                        <button
                            onClick={() => alert('Mobile menu feature can be implemented here.')}
                            className="text-white focus:outline-none"
                        >
                            ☰
                        </button>
                    </div>
                )}

                {/* Logout Button */}
                {isLoggedIn && (
                    <button
                        onClick={handleLogout}
                        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
                    >
                        Logout
                    </button>
                )}
            </div>
        </header>
    );
};

export default Header;
