import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000'; // Change this if deployed

// Upload a PDF file
export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file); // ✅ Must match `request.files['file']` in app.py

  try {
    const response = await axios.post(`${API_BASE}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response;
  } catch (error) {
    throw error;
  }
};

// Ask a question based on uploaded PDF content
export const askQuestion = async (question) => {
  try {
    const response = await axios.post(`${API_BASE}/ask`, { question });
    return response;
  } catch (error) {
    throw error;
  }
};
