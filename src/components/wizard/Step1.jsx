import React from 'react';

const Step1 = ({ formData = {}, setFormData, nextStep }) => {
    const { projectName = '', description = '' } = formData;

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleNext = () => {
        if (!projectName || !description) {
            alert('Please fill out all fields before proceeding.');
            return;
        }
        nextStep();
    };

    return (
        <div className="container mx-auto p-6">
            <h2 className="text-2xl font-bold mb-4">Step 1: Basic Information</h2>
            <form className="bg-white p-6 rounded shadow">
                <div className="mb-4">
                    <label htmlFor="projectName" className="block text-sm font-medium text-gray-700">
                        Project Name
                    </label>
                    <input
                        type="text"
                        id="projectName"
                        name="projectName"
                        value={projectName}
                        onChange={handleChange}
                        placeholder="Enter project name"
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                        Description
                    </label>
                    <textarea
                        id="description"
                        name="description"
                        value={description}
                        onChange={handleChange}
                        placeholder="Enter project description"
                        required
                        className="mt-1 block w-full px-4 py-2 border rounded"
                    ></textarea>
                </div>
                <button
                    type="button"
                    onClick={handleNext}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Next
                </button>
            </form>
        </div>
    );
};

export default Step1;
