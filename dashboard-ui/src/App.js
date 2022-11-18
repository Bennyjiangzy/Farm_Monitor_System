import logo from './logo.png';
import './App.css';

import EndpointAudit from './components/EndpointAudit'
import AppStats from './components/AppStats'
import ServiceStatus from './components/ServiceStatus'

function App() {

    const endpoints = ["farms/res", "farms/env"]

    const rendered_endpoints = endpoints.map((endpoint) => {
        return <EndpointAudit key={endpoint} endpoint={endpoint}/>
    })

    return (
        <div className="App">
            <img src={logo} className="App-logo" alt="logo" height="150px" width="400px"/>
            <div>
                <ServiceStatus/>
                <h1>Audit Endpoints</h1>
                <AppStats/>
                <h1>Audit Endpoints</h1>
                {rendered_endpoints}
            </div>
        </div>
    );

}



export default App;
