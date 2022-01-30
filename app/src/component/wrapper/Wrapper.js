import PropTypes from 'prop-types';
import './wrapper.css';

const Wrapper = (props) => {
    const { children } = props;
    return (
        <div className="wrapper">
            {children}
        </div>
    );

};

Wrapper.propTypes = {
    children: PropTypes.node
};

Wrapper.defaultProps = {
    children: null
};
export default Wrapper;