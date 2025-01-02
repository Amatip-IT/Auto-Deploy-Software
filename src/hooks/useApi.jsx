import axios from 'axios';

const useApi = () => {
    const api = axios.create({
        baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    // Attach auth token to every request if available
    api.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('authToken');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    // Handle responses and errors globally
    api.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response?.status === 401) {
                // If unauthorized, clear local storage and redirect to login
                localStorage.removeItem('authToken');
                localStorage.removeItem('user');
                window.location.href = '/';
            }
            return Promise.reject(error);
        }
    );

    return api;
};

export default useApi;
