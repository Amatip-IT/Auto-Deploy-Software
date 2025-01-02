// src/components/dashboard/Dashboard.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    // Fetch user and project data on component mount
    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch user information
                const token = localStorage.getItem('authToken');
                if (!token) {
                    navigate('/login'); // Redirect to login if not authenticated
                    return;
                }

                const userResponse = await axios.get('/api/user/profile', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setUser(userResponse.data);

                // Fetch user's projects
                const projectResponse = await axios.get('/api/projects', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setProjects(projectResponse.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to load data. Please try again.');
                setLoading(false);
            }
        };

        fetchData();
    }, [navigate]);

    // Handle logout
    const handleLogout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-100">
            <header className="bg-blue-500 text-white p-4">
                <div className="container mx-auto flex justify-between items-center">
                    <h1 className="text-lg font-bold">Dashboard</h1>
                    <div>
                        <span className="mr-4">
                            Welcome, {user ? user.name : 'Loading...'}
                        </span>
                        <button
                            onClick={handleLogout}
                            className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="container mx-auto p-6">
                {loading && <p className="text-center text-gray-700">Loading...</p>}
                {error && (
                    <div className="bg-red-100 text-red-700 p-3 mb-4 rounded text-center">
                        {error}
                    </div>
                )}
                {!loading && !error && (
                    <>
                        <h2 className="text-2xl font-bold mb-4">Your Projects</h2>
                        {projects.length > 0 ? (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                {projects.map((project) => (
                                    <div
                                        key={project.id}
                                        className="bg-white shadow-lg rounded p-4"
                                    >
                                        <h3 className="font-semibold text-lg mb-2">
                                            {project.name}
                                        </h3>
                                        <p className="text-gray-700 mb-4">
                                            {project.description}
                                        </p>
                                        <button
                                            onClick={() =>
                                                navigate(`/projects/${project.id}`)
                                            }
                                            className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
                                        >
                                            View Details
                                        </button>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-gray-700">
                                You have no projects.{' '}
                                <a
                                    href="/projects/new"
                                    className="text-blue-500 hover:underline"
                                >
                                    Create a new project
                                </a>
                                .
                            </p>
                        )}
                    </>
                )}
            </main>
        </div>
    );
};

export default Dashboard;
