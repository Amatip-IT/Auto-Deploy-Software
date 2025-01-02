// import api from './api';

// // Fetch all deployments
// export const fetchDeployments = async () => {
//     const response = await api.get('/deployments');
//     return response.data; // { deployments: [...] }
// };

// // Fetch logs for a specific deployment
// export const fetchDeploymentLogs = async (deploymentId) => {
//     const response = await api.get(`/deployments/${deploymentId}/logs`);
//     return response.data; // { logs: [...] }
// };

// // Create a new deployment
// export const createDeployment = async (deploymentData) => {
//     const response = await api.post('/deployments', deploymentData);
//     return response.data; // { id, name, description, ... }
// };

// // Delete a deployment
// export const deleteDeployment = async (deploymentId) => {
//     const response = await api.delete(`/deployments/${deploymentId}`);
//     return response.data; // { message: 'Deployment deleted successfully' }
// };
