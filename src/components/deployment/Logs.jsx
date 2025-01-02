import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Logs = () => {
    const { deploymentId } = useParams(); // Get deployment ID from the URL
    const [logs, setLogs] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLogs = async () => {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError('Authentication required. Please log in.');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const response = await axios.get(
                    `${process.env.REACT_APP_API_BASE_URL}/deployments/${deploymentId}/logs`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                setLogs(response.data.logs || []);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch logs. Please try again.');
                setLoading(false);
            }
        };

        fetchLogs();
    }, [deploymentId]);

    const filteredLogs = logs.filter((log) =>
        log.message.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-4">Deployment Logs</h2>

            {error && (
                <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">
                    {error}
                </div>
            )}

            {loading && <p className="text-center text-gray-700">Loading logs...</p>}

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
                                        <p className={`text-md font-medium text-${log.level === 'error' ? 'red-500' : 'gray-800'}`}>
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
