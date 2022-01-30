export const getNumberAmountFormat = (amount) => {
    return new Intl.NumberFormat("th-TH").format(amount);
};