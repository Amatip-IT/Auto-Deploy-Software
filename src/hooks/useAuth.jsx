import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const useAuth = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (!token) {
            // If no token is found, redirect to login
            navigate('/');
        }
    }, [navigate]);

    const logout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        navigate('/');
    };

    const isLoggedIn = !!localStorage.getItem('authToken');

    return { isLoggedIn, logout };
};

export default useAuth;
