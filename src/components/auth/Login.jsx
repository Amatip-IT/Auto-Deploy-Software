// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';

// const Login = () => {
//     // DEVELOPMENT DEFAULT CREDENTIALS - REMOVE BEFORE PRODUCTION
//     const defaultDevEmail = 'admin@admin';
//     const defaultDevPassword = 'admin';
//     // END OF DEVELOPMENT DEFAULT CREDENTIALS - REMOVE BEFORE PRODUCTION

//     const [email, setEmail] = useState(defaultDevEmail); // Default email
//     const [password, setPassword] = useState(defaultDevPassword); // Default password
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState('');
//     const navigate = useNavigate();

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setLoading(true);
//         setError('');

//         try {
//             const response = await axios.post(
//                 `${process.env.REACT_APP_API_BASE_URL}/auth/login`,
//                 { email, password },
//                 { headers: { 'Content-Type': 'application/json' } }
//             );
//             console.log('API Response:', response.data); // Debugging response
//             const { token, user } = response.data;

//             localStorage.setItem('authToken', token);
//             localStorage.setItem('user', JSON.stringify(user));

//             setLoading(false);
//             navigate('/dashboard'); // Redirect to dashboard
//         } catch (err) {
//             console.error('Login Error:', err.response || err.message); // Debugging error
//             setLoading(false);
//             setError(err.response?.data?.message || 'Network error. Please try again.');
//         }
//     };

//     return (
//         <div className="flex items-center justify-center h-screen bg-gray-100">
//             <div className="w-full max-w-md p-6 bg-white rounded shadow">
//                 <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
//                 {error && <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">{error}</div>}
//                 <form onSubmit={handleSubmit}>
//                     <input
//                         type="email"
//                         value={email}
//                         onChange={(e) => setEmail(e.target.value)}
//                         placeholder="Email"
//                         required
//                         className="w-full mb-4 px-4 py-2 border rounded"
//                     />
//                     <input
//                         type="password"
//                         value={password}
//                         onChange={(e) => setPassword(e.target.value)}
//                         placeholder="Password"
//                         required
//                         className="w-full mb-4 px-4 py-2 border rounded"
//                     />
//                     <button
//                         type="submit"
//                         className={`w-full bg-blue-500 text-white py-2 rounded ${
//                             loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
//                         }`}
//                         disabled={loading}
//                     >
//                         {loading ? 'Logging in...' : 'Login'}
//                     </button>
//                 </form>
//                 <p className="text-center text-sm mt-4">
//                     Don’t have an account?{' '}
//                     <a href="/register" className="text-blue-500 hover:underline">Register</a>
//                 </p>
//             </div>
//         </div>
//     );
// };

// export default Login;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('admin@admin'); // Default email for development
    const [password, setPassword] = useState('admin'); // Default password for development
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            // Simulate a delay to mimic API call
            await new Promise((resolve) => setTimeout(resolve, 1000));

            // Mocked response
            const token = 'mock-token';
            const user = { id: 1, name: 'Admin User', email };

            // Save token and user info
            localStorage.setItem('authToken', token);
            localStorage.setItem('user', JSON.stringify(user));

            setLoading(false);
            navigate('/dashboard'); // Redirect to dashboard
        } catch (err) {
            setLoading(false);
            setError('An unexpected error occurred. Please try again.');
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded shadow">
                <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
                {error && <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                        className="w-full mb-4 px-4 py-2 border rounded"
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
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
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
                <p className="text-center text-sm mt-4">
                    Don’t have an account?{' '}
                    <a href="/register" className="text-blue-500 hover:underline">Register</a>
                </p>
            </div>
        </div>
    );
};

export default Login;
