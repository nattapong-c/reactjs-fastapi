import * as TYPES from '../type/product';
import * as API from '../api/product';

export const getProducts = (params) => async (dispatch) => {
    dispatch({ type: TYPES.PRODUCT_LIST_REQ });
    try {
        const response = await API.getProducts(params);
        if (response.status === 200) {
            dispatch({ type: TYPES.PRODUCT_LIST_SUCCESS, payload: response });
        } else {
            dispatch({ type: TYPES.PRODUCT_LIST_FAIL, payload: response.response.data.detail });
        }
    } catch (error) {
        dispatch({ type: TYPES.PRODUCT_LIST_FAIL, payload: error });
    }
};

export const clearProducts = () => async (dispatch) => {
    dispatch({ type: TYPES.PRODUCT_LIST_CLEAR });
};



export const getProductInfo = (id) => async (dispatch) => {
    dispatch({ type: TYPES.PRODUCT_INFO_REQ });
    try {
        const response = await API.getProductInfo(id);
        if (response.status === 200) {
            dispatch({ type: TYPES.PRODUCT_INFO_SUCCESS, payload: response });
        } else {
            dispatch({ type: TYPES.PRODUCT_INFO_FAIL, payload: response.response.data.detail });
        }
    } catch (error) {
        dispatch({ type: TYPES.PRODUCT_INFO_FAIL, payload: error });
    }
};


export const buyProduct = (data) => async (dispatch) => {
    dispatch({ type: TYPES.PRODUCT_BUY_REQ });
    try {
        const response = await API.buyProduct(data);
        if (response.status === 200) {
            dispatch({ type: TYPES.PRODUCT_BUY_SUCCESS, payload: response });
        } else {
            dispatch({ type: TYPES.PRODUCT_BUY_FAIL, payload: response.response.data.detail });
        }
    } catch (error) {
        dispatch({ type: TYPES.PRODUCT_BUY_FAIL, payload: error });
    }
};

export const clearBuyProduct = () => async (dispatch) => {
    dispatch({ type: TYPES.PRODUCT_BUY_CLEAR });
};