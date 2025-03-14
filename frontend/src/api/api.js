import axios from "axios";

const API_BASE_URL = process.env.FASTAPI_APP_API_BASE_URL || "http://127.0.0.1:8000";
console.log(API_BASE_URL)
export const getUsers = async () => {
    const response = await axios.get(`${API_BASE_URL}/users/`);
    return response.data;
};

export const getRecommendations = async (userId) => {
    const response = await axios.get(`${API_BASE_URL}/recommendations?user_id=${userId}`);
    return response.data;
};

export const getProducts = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/products/`);
        console.log("API Response:", response.data); // Debugging
        return response.data;
    } catch (error) {
        console.error("API request error:", error.response?.data || error.message);
        throw error;
    }
};


export const createProduct = async (productData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/products/`, productData, {
            headers: { "Content-Type": "application/json" },
        });
        console.log("Product created:", response.data); // Debugging
        return response.data;
    } catch (error) {
        console.error("Error creating product:", error.response?.data || error.message);
        throw error;
    }
};