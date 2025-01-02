import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
// import DeploymentForm from './components/deployment/DeploymentForm';
// import Logs from './components/deployment/Logs';
// import Analytics from './components/dashboard/Analytics';
import Header from './components/Header';
// import Step1 from './components/wizard/Step1';
// import Step2 from './components/wizard/Step2';
// import StepSummary from './components/wizard/StepSummary';

const App = () => {
    return (
        <div className="min-h-screen bg-gray-100">
            {/* Header should be outside Routes */}
            <Header />
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<Dashboard />} />
                {/* Uncomment these lines when the components are ready */}
                {/* <Route path="/deployment/new" element={<DeploymentForm />} />
                <Route path="/deployment/logs" element={<Logs />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/wizard/step1" element={<Step1 />} />
                <Route path="/wizard/step2" element={<Step2 />} />
                <Route path="/wizard/summary" element={<StepSummary />} /> */}
            </Routes>
        </div>
    );
};

export default App;
