import 'antd/dist/antd.css';
import './App.css';
import { Route } from 'react-router-dom';
import { BrowserRouter, Switch } from 'react-router-dom';
import { BackTop } from 'antd';
import Error from './components/error';
import Home from './components/home';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path='*' component={Error} />
        </Switch>
      </BrowserRouter>
      <BackTop />
    </div>
  );
}

export default App;
