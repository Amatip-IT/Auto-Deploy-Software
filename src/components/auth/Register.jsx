import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Register = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess(false);

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match.');
            setLoading(false);
            return;
        }

        try {
            // Make a POST request to the backend register endpoint
            const response = await axios.post(
                `${process.env.REACT_APP_API_BASE_URL}/auth/register`,
                {
                    name: formData.name,
                    email: formData.email,
                    password: formData.password,
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            );

            setSuccess(true);
            setLoading(false);

            // Redirect to login page
            setTimeout(() => {
                navigate('/');
            }, 2000);
        } catch (err) {
            setLoading(false);
            if (err.response && err.response.data) {
                setError(err.response.data.message || 'Registration failed.');
            } else {
                setError('Network error. Please try again.');
            }
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded shadow">
                <h2 className="text-2xl font-bold text-center mb-6">Register</h2>
                {error && (
                    <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">
                        {error}
                    </div>
                )}
                {success && (
                    <div className="bg-green-100 text-green-700 p-3 mb-4 rounded">
                        Registration successful! Redirecting...
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Name"
                        required
                        className="w-full mb-4 px-4 py-2 border rounded"
                    />
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Email"
                        required
                        className="w-full mb-4 px-4 py-2 border rounded"
                    />
                    <input
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Password"
                        required
                        className="w-full mb-4 px-4 py-2 border rounded"
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        placeholder="Confirm Password"
                        required
                        className="w-full mb-4 px-4 py-2 border rounded"
                    />
                    <button
                        type="submit"
                        className={`w-full bg-blue-500 text-white py-2 rounded ${
                            loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
                        }`}
                        disabled={loading}
                    >
                        {loading ? 'Registering...' : 'Register'}
                    </button>
                </form>
                <p className="text-center text-sm mt-4">
                    Already have an account?{' '}
                    <a href="/" className="text-blue-500 hover:underline">
                        Login
                    </a>
                </p>
            </div>
        </div>
    );
};

export default Register;
