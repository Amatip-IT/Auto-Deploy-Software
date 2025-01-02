import React from 'react';
import { useNavigate } from 'react-router-dom';

const StepSummary = ({ previousStep }) => {
    const navigate = useNavigate();

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-4">You're All Set!</h2>
            <p className="text-gray-700 mb-6">
                You've completed the wizard. Here are some next steps to get started with Auto Deploy Software:
            </p>
            <ul className="list-disc pl-6 mb-6">
                <li>
                    <strong>Deploy Your First App:</strong>{' '}
                    <button
                        onClick={() => navigate('/deployment/new')}
                        className="text-blue-500 hover:underline"
                    >
                        Start Deployment
                    </button>
                </li>
                <li>
                    <strong>View Analytics:</strong>{' '}
                    <button
                        onClick={() => navigate('/analytics')}
                        className="text-blue-500 hover:underline"
                    >
                        Explore Analytics
                    </button>
                </li>
                <li>
                    <strong>Monitor Logs:</strong>{' '}
                    <button
                        onClick={() => navigate('/deployment/logs')}
                        className="text-blue-500 hover:underline"
                    >
                        Check Logs
                    </button>
                </li>
            </ul>
            <div className="flex justify-between">
                <button
                    onClick={previousStep}
                    className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                >
                    Previous
                </button>
                <button
                    onClick={() => navigate('/dashboard')}
                    className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                    Go to Dashboard
                </button>
            </div>
        </div>
    );
};

export default StepSummary;
