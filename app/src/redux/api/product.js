import axios from 'axios';
import ENV from '../../env.json';

export const getProducts = async (params) => {
    try {
        return await axios.get(`${ENV.API_URL}/product/${params}`, {
            headers: {
                'content-type': 'application/json',
            },
        });
    } catch (error) {
        return error;
    }
};

export const getProductInfo = async (id) => {
    try {
        return await axios.get(`${ENV.API_URL}/product/${id}`, {
            headers: {
                'content-type': 'application/json',
            },
        });
    } catch (error) {
        return error;
    }
};


export const buyProduct = async (data) => {
    try {
        return await axios.post(`${ENV.API_URL}/payment`, data, {
            headers: {
                'content-type': 'application/json',
            },
        });
    } catch (error) {
        return error;
    }
};