import React, { useState } from 'react';
import './App.css';
import PersonGenerator from './components/PersonGenerator';
import PersonHabitDashboard from './components/PersonHabitDashboard/PersonHabitDashboard';
import Log from './components/Log/Log';
import Header from './components/Header/Header';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';


const App = () => {
    const [logMessages, setLogMessages] = useState([]);

    return (
    <div className="App">
      <Header />
      <AdminDashboard setLogMessages={setLogMessages} />
      <Log messages={logMessages} />

    </div>
    );
}

export default App;

/*
<PersonGenerator setLogMessages={setLogMessages} />
<PersonHabitDashboard setLogMessages={setLogMessages} />
*/