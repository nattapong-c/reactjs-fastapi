import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import * as todoActions from '../../redux/action/product';
import Loading from '../../component/loading/Loading';
import Error from '../../component/error/Error';
import './index.css';
import { Button, Modal } from 'antd';
import { getNumberAmountFormat } from '../../utils/number';

const coin = [1, 5, 10];
const banknote = [20, 50, 100, 500, 1000];
const getBuyError = (error, availableChanges, expectedChanges) => {
    switch (error) {
        case "change not enough": {
            let text = 'เงินทอนไม่เพียงพอ';
            if (availableChanges > 0) text += ` คุณจะได้รับเงินทอน ${getNumberAmountFormat(availableChanges)} บาท จาก ${getNumberAmountFormat(expectedChanges)} บาท`;
            return text + ' ต้องการทำรายการต่อหรือไม่?'
        }
        case "product out of stock": {
            return "สินค้าหมด";
        }
        default: return 'ติดต่อเจ้าหน้าที่';
    }
};

const ProductInfo = () => {
    const { id } = useParams();
    const dispatch = useDispatch();
    const loading = useSelector((state) => state.product_info.loading);
    const error = useSelector((state) => state.product_info.error);
    const info = useSelector((state) => state.product_info.info);
    const buyLoading = useSelector((state) => state.buy_info.loading);
    const buyError = useSelector((state) => state.buy_info.error);
    const buyInfo = useSelector((state) => state.buy_info.info);

    const [isBuyStage, setIsBuyState] = useState(false);
    const [amount, setAmount] = useState(0);
    const [usedMoney, setUsedMoney] = useState({});
    const [buyAlert, setBuyAlert] = useState(false);
    const [errorAlert, setErrorAlert] = useState(false);

    useEffect(() => {
        dispatch(todoActions.getProductInfo(id));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        if (buyError?.can_accept) {
            setBuyAlert(true);
        } else if (buyError?.error) {
            setErrorAlert(true);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [buyError]);

    const onClickMoney = (moneyAmount) => {
        let used = usedMoney;
        let amountStr = moneyAmount + "";
        if (amountStr in used) {
            used[amountStr] = usedMoney[amountStr] + 1;
        } else {
            used[amountStr] = 1;
        }
        let totalAmount = amount + moneyAmount;
        setAmount(totalAmount);
        setUsedMoney(used);
        if (totalAmount >= info?.price) setBuyAlert(true);
    };

    const clearAmount = (clear, refresh) => {
        setAmount(0);
        setUsedMoney({});
        setBuyAlert(false);
        setIsBuyState(false);
        clear && dispatch(todoActions.clearBuyProduct());
        refresh && dispatch(todoActions.getProductInfo(id));
    };

    const buyProduct = (acceptChanges) => {
        let data = {
            product_id: info?._id,
            used_money: usedMoney,
            accept_changes: acceptChanges
        };
        dispatch(todoActions.buyProduct(data));
        setBuyAlert(false);
    };

    const renderChanges = (usedMoneyChanges) => {
        let amount = Object.keys(usedMoneyChanges);
        if (amount.length > 0) {
            return amount.map(a => (
                <p key={a}>{a < 20 ? "เหรียญ" : "ธนบัตร"} {a} บาท: <span className='amount-count'>{usedMoneyChanges[a]} {a < 20 ? "เหรียญ" : "ใบ"}</span></p>
            ));
        }
    };

    return (
        <>
            <Loading show={loading || buyLoading} />
            {error && <Error message={error} />}
            <div style={{ padding: "20px" }}>
                <Button><Link to="/">กลับไปหน้าแรก</Link></Button>
            </div>
            <div className='product-info'>
                <div className='col image'>
                    <img alt='' src='' />
                </div>
                <div className='col info'>
                    <h1>{info?.name}</h1>
                    <p className='price'>{info?.price ? getNumberAmountFormat(info.price) : "-"} บาท</p>
                    <div className='tag'>{info?.category}</div>
                    {info?.stock > 0 ? (<p className='stock'>เหลือ {info?.stock} ชิ้น</p>) : (<p className='stock out-of-stock'>OUT OF STOCK</p>)}
                    <div className={`buy-section ${isBuyStage ? 'buying' : 'default'}`}>
                        <Modal visible={buyAlert} onCancel={() => clearAmount(false)} onOk={() => buyProduct(false)} cancelText="คืนเงิน" okText="ยืนยัน" closable={false}>
                            ยืนยันการซื้อ
                        </Modal>
                        <Modal visible={buyAlert && buyError !== null} onCancel={() => clearAmount(true)} onOk={() => buyProduct(true)} cancelText="คืนเงิน" okText="ยืนยัน" closable={false}>
                            {getBuyError(buyError?.error, buyError?.available_changes, buyError?.expected_changes)}
                        </Modal>
                        <Modal visible={errorAlert && buyError !== null}
                            closable={false}
                            footer={[
                                <Button key="ok" onClick={() => clearAmount(true, true)}>ปิด</Button>
                            ]}>
                            {getBuyError(buyError?.error)}
                        </Modal>
                        <Modal
                            visible={buyError === null && buyInfo !== null}
                            closable={false}
                            footer={[
                                <Button key="ok" onClick={() => clearAmount(true, true)}>ปิด</Button>
                            ]}
                        >
                            <p className='thankyou-text'>ขอบคุณที่ใช้บริการ</p>
                            {buyInfo?.available_changes > 0 && (<p>รับเงินทอน {getNumberAmountFormat(buyInfo?.available_changes)} บาท</p>)}
                            {buyInfo?.used_changes && renderChanges(buyInfo?.used_changes)}
                        </Modal>
                        {isBuyStage ? (
                            <div>
                                <div style={{ marginTop: "40px" }}>
                                    <p className='buy-amount'>{getNumberAmountFormat(amount)} บาท</p>
                                </div>
                                <div className='money'>
                                    <div>
                                        {coin.map(c => (<Button className={`coin b${c}`} key={c} onClick={() => onClickMoney(c)}>{c}</Button>))}
                                    </div>
                                    <div className='banknote-wrapper'>
                                        {banknote.map(b => (<Button className={`banknote b${b}`} key={b} onClick={() => onClickMoney(b)}>{b}</Button>))}
                                    </div>
                                    <div style={{ marginTop: "15px" }}>
                                        <Button onClick={() => clearAmount()}>คืนเงิน</Button>
                                    </div>
                                </div>
                            </div>
                        ) : info?.stock > 0 && (
                            <Button type='primary' onClick={() => setIsBuyState(true)}>จ่ายเงิน</Button>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
};

export default ProductInfo;