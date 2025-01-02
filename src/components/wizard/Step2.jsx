import React from 'react';

const Step2 = ({ nextStep, previousStep }) => {
    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-4">Explore Core Features</h2>
            <p className="text-gray-700 mb-6">
                Auto Deploy Software offers a range of features to streamline your application deployment:
            </p>
            <ul className="list-disc pl-6 mb-6">
                <li>
                    <strong>Deployment Automation:</strong> Easily deploy from GitHub repositories or local projects with just a few clicks.
                </li>
                <li>
                    <strong>Monitoring and Logs:</strong> Track deployment progress and debug issues using the detailed logs viewer.
                </li>
                <li>
                    <strong>Analytics:</strong> Get insights into deployment performance, latency, and traffic.
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
                    onClick={nextStep}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Next: Summary
                </button>
            </div>
        </div>
    );
};

export default Step2;
