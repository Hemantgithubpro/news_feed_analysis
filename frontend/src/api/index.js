import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getFeeds = () => api.get('/feeds');
export const addFeed = (url, name) => api.post('/feeds', { url, name });
export const deleteFeed = (id) => api.delete(`/feeds/${id}`);
export const refreshFeed = (id) => api.post(`/feeds/${id}/refresh`);

export const getArticles = (params) => api.get('/articles', { params });
export const getArticle = (id) => api.get(`/articles/${id}`);
export const getSentimentStats = () => api.get('/articles/stats/sentiment');

export default api;
