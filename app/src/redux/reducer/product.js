import * as TYPES from '../type/product';

const listState = {
    loading: false,
    error: null,
    products: [],
    total_item: 0,
    total_page: 0
};

const infoState = {
    loading: false,
    error: null,
    info: null
};

const buyState = {
    loading: false,
    error: null,
    info: null,
};

export const productListReducer = (state = listState, { type, payload }) => {
    switch (type) {
        case TYPES.PRODUCT_LIST_REQ:
            return { ...state, loading: true };
        case TYPES.PRODUCT_LIST_SUCCESS:
            return { ...state, loading: false, error: null, products: state.products.concat(payload.data.data.products), total_item: payload.data.data.total_item, total_page: payload.data.data.total_page };
        case TYPES.PRODUCT_LIST_CLEAR:
            return { ...state, loading: false, error: null, products: [], total_item: 0, total_page: 0 };
        case TYPES.PRODUCT_LIST_FAIL:
            return { ...state, loading: false, error: payload, products: [], total_item: 0, total_page: 0 };
        default:
            return state;
    }
}

export const productInfoReducer = (state = infoState, { type, payload }) => {
    switch (type) {
        case TYPES.PRODUCT_INFO_REQ:
            return { ...state, loading: true };
        case TYPES.PRODUCT_INFO_SUCCESS:
            return { ...state, loading: false, error: null, info: payload.data.data };
        case TYPES.PRODUCT_INFO_FAIL:
            return { ...state, loading: false, error: payload, info: null };
        default:
            return state;
    }
}


export const productBuyReducer = (state = buyState, { type, payload }) => {
    switch (type) {
        case TYPES.PRODUCT_BUY_REQ:
            return { ...state, loading: true };
        case TYPES.PRODUCT_BUY_SUCCESS:
            return { ...state, loading: false, error: null, info: payload.data.data };
        case TYPES.PRODUCT_BUY_FAIL:
            return { ...state, loading: false, error: payload, info: null };
        case TYPES.PRODUCT_BUY_CLEAR:
            return { ...state, loading: false, error: null, info: null };
        default:
            return state;
    }
}