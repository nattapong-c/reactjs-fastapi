import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Provider } from 'react-redux';
import CustomRoutes from './route/Route';
import store from './redux';
import './App.css';

const App = () => {
  return (
    <Provider store={store}>
      <Router>
        <CustomRoutes />
      </Router>
    </Provider>
  );
};

export default App;
