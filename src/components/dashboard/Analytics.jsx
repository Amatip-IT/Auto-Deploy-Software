import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Analytics = () => {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAnalytics = async () => {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError('Authentication required. Please log in.');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const response = await axios.get(
                    `${process.env.REACT_APP_API_BASE_URL}/analytics`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                setAnalyticsData(response.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch analytics. Please try again.');
                setLoading(false);
            }
        };

        fetchAnalytics();
    }, []);

    if (loading) {
        return <p className="text-center text-gray-700">Loading analytics...</p>;
    }

    if (error) {
        return (
            <div className="bg-red-100 text-red-700 p-3 mb-4 rounded text-center">
                {error}
            </div>
        );
    }

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-6">Deployment Analytics</h2>

            {/* Analytics Overview */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-lg font-bold">Total Deployments</h3>
                    <p className="text-3xl font-semibold text-blue-500">
                        {analyticsData?.totalDeployments || 0}
                    </p>
                </div>
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-lg font-bold">Active Deployments</h3>
                    <p className="text-3xl font-semibold text-green-500">
                        {analyticsData?.activeDeployments || 0}
                    </p>
                </div>
                <div className="bg-white p-4 rounded shadow">
                    <h3 className="text-lg font-bold">Failed Deployments</h3>
                    <p className="text-3xl font-semibold text-red-500">
                        {analyticsData?.failedDeployments || 0}
                    </p>
                </div>
            </div>

            {/* Traffic and Performance */}
            <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">Traffic and Performance</h3>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="bg-white p-4 rounded shadow">
                        <h4 className="text-lg font-bold">Global Traffic</h4>
                        <p className="text-xl font-semibold text-gray-700">
                            {analyticsData?.globalTraffic || 'N/A'} visits
                        </p>
                        <p className="text-sm text-gray-600">
                            Data reflects traffic across all deployments.
                        </p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h4 className="text-lg font-bold">Average Latency</h4>
                        <p className="text-xl font-semibold text-gray-700">
                            {analyticsData?.averageLatency || 'N/A'} ms
                        </p>
                        <p className="text-sm text-gray-600">
                            Average response time across all deployments.
                        </p>
                    </div>
                </div>
            </div>

            {/* Deployment Status Breakdown */}
            <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">Deployment Status Breakdown</h3>
                {analyticsData?.deploymentStatus ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {analyticsData.deploymentStatus.map((status) => (
                            <div
                                key={status.name}
                                className={`p-4 rounded shadow ${
                                    status.count > 0
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-gray-100 text-gray-800'
                                }`}
                            >
                                <h4 className="text-lg font-bold">{status.name}</h4>
                                <p className="text-xl font-semibold">{status.count}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-600">
                        No deployment status data available at the moment.
                    </p>
                )}
            </div>
        </div>
    );
};

export default Analytics;
