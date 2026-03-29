import axios from 'axios';
import type { AxiosInstance } from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API 함수들
export const loginApi = {
  login: (username: string, password: string) =>
    apiClient.get('/login', {
      params: { username, password },
    }),
};

export const boardApi = {
  getPosts: () => apiClient.get('/board'),
  addPost: (name: string, content: string) =>
    apiClient.post('/board', { name, content }, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
};
