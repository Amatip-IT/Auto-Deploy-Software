import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import useAuth from '../hooks/useAuth';

const Dashboard = () => {
    const { isLoggedIn, logout } = useAuth(); // Use authentication hook
    const [user, setUser] = useState(null);
    const [deployments, setDeployments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Fetch user and deployments
    useEffect(() => {
        const fetchData = async () => {
            if (!isLoggedIn) {
                navigate('/'); // Redirect if not logged in
                return;
            }

            try {
                setLoading(true);
                const token = localStorage.getItem('authToken');

                // Fetch user data
                const userResponse = await axios.get(
                    `${process.env.REACT_APP_API_BASE_URL}/user/profile`,
                    {
                        headers: { Authorization: `Bearer ${token}` },
                    }
                );
                setUser(userResponse.data);

                // Fetch deployment data
                const deploymentsResponse = await axios.get(
                    `${process.env.REACT_APP_API_BASE_URL}/deployments`,
                    {
                        headers: { Authorization: `Bearer ${token}` },
                    }
                );
                setDeployments(deploymentsResponse.data.deployments || []);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch data. Please try again.');
                setLoading(false);
            }
        };

        fetchData();
    }, [isLoggedIn, navigate]);

    return (
        <div className="container mx-auto p-6">
            {loading && <p className="text-center text-gray-700">Loading...</p>}
            {error && (
                <div className="bg-red-100 text-red-700 p-3 mb-4 rounded text-center">
                    {error}
                </div>
            )}
            {!loading && !error && (
                <>
                    {/* User Welcome */}
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">
                            Welcome, {user?.name || 'User'}!
                        </h2>
                        <button
                            onClick={logout}
                            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                        >
                            Logout
                        </button>
                    </div>

                    {/* Deployment Actions */}
                    <div className="mb-6">
                        <Link
                            to="/deployment/new"
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-4"
                        >
                            New Deployment
                        </Link>
                        <Link
                            to="/analytics"
                            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                        >
                            View Analytics
                        </Link>
                    </div>

                    {/* Deployment List */}
                    <div>
                        <h3 className="text-xl font-bold mb-4">Your Deployments</h3>
                        {deployments.length > 0 ? (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                {deployments.map((deployment) => (
                                    <div
                                        key={deployment.id}
                                        className="bg-white p-4 rounded shadow hover:shadow-lg"
                                    >
                                        <h4 className="text-lg font-semibold">
                                            {deployment.name}
                                        </h4>
                                        <p className="text-sm text-gray-600">
                                            {deployment.description || 'No description provided.'}
                                        </p>
                                        <div className="mt-4">
                                            <Link
                                                to={`/deployment/logs/${deployment.id}`}
                                                className="text-blue-500 hover:underline"
                                            >
                                                View Logs
                                            </Link>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="text-gray-600">You have no deployments yet.</p>
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;
