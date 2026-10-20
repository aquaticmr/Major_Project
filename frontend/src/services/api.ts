import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setupAxiosAuth = (getToken: () => Promise<string | null>) => {
  apiClient.interceptors.request.use(async (config) => {
    try {
      const token = await getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      } else {
        // Fallback for local demo mode if no Clerk publishable key configured yet
        config.headers.Authorization = `Bearer test_token_local_user`;
      }
    } catch (e) {
      console.warn("Failed retrieving Clerk token:", e);
      config.headers.Authorization = `Bearer test_token_local_user`;
    }
    return config;
  }, (error) => {
    return Promise.reject(error);
  });
};
