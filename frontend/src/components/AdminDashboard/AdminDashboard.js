import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PersonCard from './PersonCard';
import PersonGenerator from '../PersonGenerator';
import './AdminDashboard.css';

const AdminDashboard = ({ setLogMessages }) => {
  const [persons, setPersons] = useState([]);

  const fetchPersons = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/persons');
      setPersons(response.data);
    } catch (error) {
      setLogMessages((prev) => [`Error fetching persons: ${error}`, ...prev]);
    }
  };

  useEffect(() => {
    fetchPersons();
  }, []);

  return (
    <div className="admin-dashboard-container">
      <div className="admin-sidebar">
        <PersonGenerator
          setLogMessages={setLogMessages}
          onGenerateComplete={fetchPersons}
        />
      </div>

      <div className="admin-main">
        <h2>Admin Dashboard</h2>
        <div className="person-cards-container">
          {persons.length > 0 ? (
            persons.map((person) => (
              <PersonCard
                key={person.person_id}
                person={person}
                setLogMessages={setLogMessages}
              />
            ))
          ) : (
            <p>No persons found.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
