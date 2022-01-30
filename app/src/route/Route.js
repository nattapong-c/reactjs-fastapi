import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProductListScreen from '../screen/product'
import ProductInfoScreen from '../screen/product/ProductInfo'
import NotFoundScreen from '../screen/404';

const CustomRoutes = () => {
    return (
        <Routes>
            <Route exact element={<ProductListScreen />} path="/" />
            <Route exact element={<ProductInfoScreen />} path="/:id" />
            <Route element={<NotFoundScreen />} path="*" />
        </Routes>
    );
};

export default CustomRoutes;