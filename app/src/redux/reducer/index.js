import { combineReducers } from 'redux';
import { productInfoReducer, productListReducer, productBuyReducer } from '../reducer/product';


const appReducer = combineReducers({
    product_list: productListReducer,
    product_info: productInfoReducer,
    buy_info: productBuyReducer
});

const rootReducer = (state, action) => {
    return appReducer(state, action);
};

export default rootReducer;