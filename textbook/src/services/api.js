// src/services/api.js
// API service to communicate with the backend embedding pipeline

const BACKEND_URL = 'https://my-doc-backend-kww0.onrender.com';  // Default backend URL

class ApiService {
  async query(question, topK = 3) {
    try {
      const response = await fetch(`${BACKEND_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query_text: question,
          top_k: topK
        })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error querying backend:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  async createCollection(collectionName) {
    try {
      const response = await fetch(`${BACKEND_URL}/create-collection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ collection_name: collectionName })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating collection:', error);
      throw error;
    }
  }
}

export default new ApiService();