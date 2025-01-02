import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import useApi from '../hooks/useApi';

const Logs = () => {
    const { deploymentId } = useParams(); // Get deployment ID from the URL
    const api = useApi(); // Use custom API hook
    const [logs, setLogs] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchLogs = async () => {
            if (!deploymentId) {
                setError('No deployment ID provided. Please select a valid deployment.');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const response = await api.get(`/deployments/${deploymentId}/logs`);
                setLogs(response.data.logs || []);
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to fetch logs.');
            } finally {
                setLoading(false);
            }
        };

        fetchLogs();
    }, [api, deploymentId]);

    const filteredLogs = logs.filter((log) =>
        log.message.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-4">Deployment Logs</h2>

            {/* Error Message */}
            {error && (
                <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">
                    {error}
                </div>
            )}

            {/* Loading Indicator */}
            {loading && <p className="text-center text-gray-700">Loading logs...</p>}

            {/* Logs Content */}
            {!loading && !error && (
                <>
                    {/* Filter Input */}
                    <div className="mb-4">
                        <input
                            type="text"
                            placeholder="Filter logs..."
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                            className="w-full px-4 py-2 border rounded"
                        />
                    </div>

                    {/* Logs Display */}
                    {filteredLogs.length > 0 ? (
                        <div className="bg-white p-4 rounded shadow">
                            <ul className="divide-y divide-gray-200">
                                {filteredLogs.map((log, index) => (
                                    <li key={index} className="py-2">
                                        <p className="text-sm text-gray-500">
                                            {new Date(log.timestamp).toLocaleString()}
                                        </p>
                                        <p
                                            className={`text-md font-medium ${
                                                log.level === 'error' ? 'text-red-500' : 'text-gray-800'
                                            }`}
                                        >
                                            {log.message}
                                        </p>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ) : (
                        <p className="text-gray-600">No logs match your filter.</p>
                    )}
                </>
            )}
        </div>
    );
};

export default Logs;
