const BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.50.71:8000';

export const API_ENDPOINTS = {
  SIGNUP: '/api/auth/signup',
  LOGIN: '/api/auth/login-json',
  RECOMMEND: '/api/recommend/',
  FEEDBACK: '/api/recommend/feedback',
  NEARBY_RESTAURANTS: '/api/recommend/nearby',
};

export default BASE_URL;
