import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Wrapper from '../../component/wrapper/Wrapper';
import ProductCard from '../../component/card/ProductCard';
import './index.css';
import * as todoActions from '../../redux/action/product';
import { Button } from 'antd';
import Loading from '../../component/loading/Loading';
import Error from '../../component/error/Error';


const SIZE = 24;
const ProductList = () => {
    const dispatch = useDispatch();
    const loading = useSelector((state) => state.product_list.loading);
    const error = useSelector((state) => state.product_list.error);
    const products = useSelector((state) => state.product_list.products);
    const totalPage = useSelector((state) => state.product_list.total_page);
    const [currentPage, setCurrentPage] = useState(1);
    const [currentCategory, setCurrentCategory] = useState("all")

    useEffect(() => {
        dispatch(todoActions.clearProducts());
        dispatch(todoActions.getProducts(`?page=1&size=${SIZE}`));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const loadMoreProduct = () => {
        let page = currentPage + 1;
        if (page > totalPage) return false;
        if (currentCategory === "all") {
            dispatch(todoActions.getProducts(`?page=${page}&size=${SIZE}`));
        } else {
            dispatch(todoActions.getProducts(`?page=${page}&size=${SIZE}&category=${currentCategory}`));
        }
        setCurrentPage(page);
    };

    const filterProduct = (category) => {
        dispatch(todoActions.clearProducts());
        if (category === "all") {
            dispatch(todoActions.getProducts(`?page=1&size=${SIZE}`));
        } else {
            dispatch(todoActions.getProducts(`?page=1&size=${SIZE}&category=${category}`));
        }
        setCurrentPage(1);
        setCurrentCategory(category);
    };

    return (
        <>
            <div className='banner'>
                <h1>Blue Vending Machine</h1>
            </div>
            <Wrapper>
                <div className='product-filter-wrapper'>
                    <div className='product-filter'>
                        <Button type={currentCategory === "all" ? "primary" : ""} onClick={() => filterProduct("all")}>All</Button>
                        <Button type={currentCategory === "food" ? "primary" : ""} onClick={() => filterProduct("food")}>Food</Button>
                        <Button type={currentCategory === "drink" ? "primary" : ""} onClick={() => filterProduct("drink")}>Drink</Button>
                        <Button type={currentCategory === "snack" ? "primary" : ""} onClick={() => filterProduct("snack")}>Snack</Button>
                    </div>
                </div>
                <div className='product-list'>
                    {error && (<Error message={error} />)}
                    {
                        products.length <= 0 ? !loading && (
                            <p>ไม่มีสินค้า</p>
                        ) : products.map(p => (
                            <ProductCard
                                key={p._id}
                                id={p._id}
                                name={p.name}
                                price={p.price}
                                stock={p.stock}
                                category={p.category}
                                image={p.image}
                            />
                        ))
                    }
                </div>
                <div className='load-more'>
                    {
                        loading ? (
                            <Loading show={loading} inline />
                        ) : currentPage !== totalPage && (
                            <Button onClick={() => loadMoreProduct()}>ดูสินค้าเพิ่ม</Button>
                        )
                    }

                </div>

            </Wrapper>
        </>
    )
};

export default ProductList;