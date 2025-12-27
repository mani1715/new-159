import api from './api';

const clientService = {
  // Get all clients
  getAllClients: async () => {
    const response = await api.get('/admin/clients/');
    return response.data;
  },

  // Get single client by ID
  getClient: async (clientId) => {
    const response = await api.get(`/admin/clients/${clientId}/`);
    return response.data;
  },

  // Create new client
  createClient: async (clientData) => {
    const response = await api.post('/admin/clients/', clientData);
    return response.data;
  },

  // Update client
  updateClient: async (clientId, clientData) => {
    const response = await api.put(`/admin/clients/${clientId}/`, clientData);
    return response.data;
  },

  // Delete client
  deleteClient: async (clientId) => {
    const response = await api.delete(`/admin/clients/${clientId}/`);
    return response.data;
  },

  // Get client projects
  getClientProjects: async (clientId) => {
    const response = await api.get(`/admin/clients/${clientId}/projects/`);
    return response.data;
  },

  // Create client project
  createClientProject: async (projectData) => {
    const response = await api.post('/admin/client-projects/', projectData);
    return response.data;
  },

  // Update client project
  updateClientProject: async (projectId, projectData) => {
    const response = await api.put(`/admin/client-projects/${projectId}/`, projectData);
    return response.data;
  },

  // Delete client project
  deleteClientProject: async (projectId) => {
    const response = await api.delete(`/admin/client-projects/${projectId}/`);
    return response.data;
  },

  // Get all client projects
  getAllClientProjects: async () => {
    const response = await api.get('/admin/client-projects/');
    return response.data;
  },

  // Upload file to project
  uploadProjectFile: async (projectId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(
      `/admin/client-projects/${projectId}/files/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    );
    return response.data;
  },

  // Delete project file
  deleteProjectFile: async (projectId, fileId) => {
    const response = await api.delete(`/admin/client-projects/${projectId}/files/${fileId}/`);
    return response.data;
  }
};

export default clientService;
