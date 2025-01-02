import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import Dashboard from "./components/dashboard/Dashboard";
import DeploymentForm from "./components/deployment/DeploymentForm";
import Logs from "./components/deployment/Logs";
import Analytics from "./components/dashboard/Analytics";
import Header from "./components/Header";
import Wizard from "./components/wizard/wizard";

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header is placed outside Routes for consistent navigation */}
      <Header />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/deployment/new" element={<DeploymentForm />} />
        <Route path="/deployment/logs" element={<Logs />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/wizard/*" element={<Wizard />} />{" "}
        {/* Routes handled by Wizard.jsx */}
      </Routes>
    </div>
  );
};

export default App;
