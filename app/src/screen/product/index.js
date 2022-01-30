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

    useEffect(() => {
        dispatch(todoActions.clearProducts());
        dispatch(todoActions.getProducts(`?page=1&size=${SIZE}`));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const loadMoreProduct = () => {
        let page = currentPage + 1;
        if (page > totalPage) return false;
        dispatch(todoActions.getProducts(`?page=${page}&size=${SIZE}`));
        setCurrentPage(page);
    };

    return (
        <>
            <Wrapper>
                <h1>เลือกสินค้า</h1>
                {error && (<Error message={error} />)}
                <div className='product-list'>
                    {
                        products.length <= 0 ? (
                            <p>ไม่มีสินค้า</p>
                        ) : products.map(p => (
                            <ProductCard key={p._id} id={p._id} name={p.name} price={p.price} stock={p.stock} category={p.category} />
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