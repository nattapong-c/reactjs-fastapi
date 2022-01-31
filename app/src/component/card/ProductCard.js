import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import './card.css';
import { Button } from 'antd';
import { getNumberAmountFormat } from '../../utils/number';

const ProductCard = (props) => {
    const { id, name, price, stock, category, image } = props;
    return (
        <>
            <div className='product-card'>
                <div className='image'>
                    <img alt='' src={"data:image/png;base64,"+image} width="200"/>
                </div>
                <div className='info'>
                    <h4>{name}</h4>
                    <p className='price'>ราคา {getNumberAmountFormat(price)} บาท</p>
                    <div className='tag'>{category}</div>
                    {stock > 0 ? (<p className='stock'>เหลือ {stock} ชิ้น</p>) : (<p className='stock out-of-stock'>OUT OF STOCK</p>)}
                    <div className='action'>
                        <Button className='button' disabled={stock <= 0}><Link to={`/${id}`}>ซื้อ</Link></Button>
                    </div>
                </div>
            </div>
        </>
    );
};

ProductCard.propTypes = {
    id: PropTypes.string,
    name: PropTypes.string,
    price: PropTypes.number,
    stock: PropTypes.number,
    category: PropTypes.string,
    image: PropTypes.string,
};

ProductCard.defaultProps = {
    id: "",
    name: "-",
    price: 0,
    stock: 0,
    category: "-",
    image: null
};

export default ProductCard;