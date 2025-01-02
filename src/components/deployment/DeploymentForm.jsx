import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const DeploymentForm = () => {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        repositoryUrl: '',
        environment: 'production',
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

        const token = localStorage.getItem('authToken');
        if (!token) {
            setError('You must be logged in to create a deployment.');
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post(
                `${process.env.REACT_APP_API_BASE_URL}/deployments`,
                formData,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );

            setSuccess(true);
            setLoading(false);

            // Redirect to logs or dashboard after successful submission
            setTimeout(() => {
                navigate(`/deployment/logs/${response.data.deploymentId}`);
            }, 2000);
        } catch (err) {
            setLoading(false);
            setError(
                err.response?.data?.message || 'Failed to create deployment. Please try again.'
            );
        }
    };

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-6">Create a New Deployment</h2>
            {error && (
                <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">
                    {error}
                </div>
            )}
            {success && (
                <div className="bg-green-100 text-green-700 p-3 mb-4 rounded">
                    Deployment created successfully! Redirecting...
                </div>
            )}
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow">
                <div className="mb-4">
                    <label
                        htmlFor="name"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Deployment Name
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Enter deployment name"
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    />
                </div>

                <div className="mb-4">
                    <label
                        htmlFor="description"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        placeholder="Enter a brief description"
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    ></textarea>
                </div>

                <div className="mb-4">
                    <label
                        htmlFor="repositoryUrl"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Repository URL
                    </label>
                    <input
                        type="url"
                        id="repositoryUrl"
                        name="repositoryUrl"
                        value={formData.repositoryUrl}
                        onChange={handleChange}
                        placeholder="https://github.com/your-repo"
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    />
                </div>

                <div className="mb-4">
                    <label
                        htmlFor="environment"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Environment
                    </label>
                    <select
                        id="environment"
                        name="environment"
                        value={formData.environment}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    >
                        <option value="production">Production</option>
                        <option value="staging">Staging</option>
                        <option value="development">Development</option>
                    </select>
                </div>

                <button
                    type="submit"
                    className={`w-full bg-blue-500 text-white py-2 rounded ${
                        loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
                    }`}
                    disabled={loading}
                >
                    {loading ? 'Creating Deployment...' : 'Create Deployment'}
                </button>
            </form>
        </div>
    );
};

export default DeploymentForm;
