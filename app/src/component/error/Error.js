import PropTypes from 'prop-types';

const ErrorMessage = (props) => {
    const { message } = props;
    return (
        <>
            <p style={{ color: "red" }}>{message}</p>
        </>
    );
};

ErrorMessage.propTypes = {
    message: PropTypes.string,
};

ErrorMessage.defaultProps = {
    message: null,
};

export default ErrorMessage;