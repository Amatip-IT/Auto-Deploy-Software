// import axios from 'axios';

// const api = axios.create({
//     baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
//     headers: {
//         'Content-Type': 'application/json',
//     },
// });

// // Attach Authorization header to all requests
// api.interceptors.request.use(
//     (config) => {
//         const token = localStorage.getItem('authToken');
//         if (token) {
//             config.headers.Authorization = `Bearer ${token}`;
//         }
//         return config;
//     },
//     (error) => Promise.reject(error)
// );

// // Global error handling
// api.interceptors.response.use(
//     (response) => response,
//     (error) => {
//         if (error.response?.status === 401) {
//             // Unauthorized: clear local storage and redirect to login
//             localStorage.removeItem('authToken');
//             localStorage.removeItem('user');
//             window.location.href = '/';
//         }
//         return Promise.reject(error);
//     }
// );

// export default api;
