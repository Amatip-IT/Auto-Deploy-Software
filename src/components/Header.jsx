import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('/'); // Redirect to the home page
    };

    return (
        <header className="bg-blue-600 text-white p-4">
            <div className="container mx-auto flex justify-between items-center">
                <h1 className="text-lg font-bold">Auto Deploy Software</h1>
                <nav className="space-x-4">
                    <Link to="/dashboard" className="hover:underline">Dashboard</Link>
                    <Link to="/deployment/new" className="hover:underline">New Deployment</Link>
                    <Link to="/analytics" className="hover:underline">Analytics</Link>
                    <button
                        onClick={handleLogout}
                        className="bg-red-500 px-4 py-2 rounded hover:bg-red-600"
                    >
                        Logout
                    </button>
                </nav>
            </div>
        </header>
    );
};

export default Header;
