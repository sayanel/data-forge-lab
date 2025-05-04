import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { faker } from '@faker-js/faker';
import axios from 'axios';

const PersonGenerator = ({ setLogMessages, onGenerateComplete }) => {
    const [numberOfPersons, setNumberOfPersons] = useState(0);
    const [generatedPersons, setGeneratedPersons] = useState([]);
    const [availableCountries, setAvailableCountries] = useState([]);

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/countries');
                setAvailableCountries(response.data);
            } catch (error) {
                setLogMessages((prevMessages) => [`Error fetching countries: ${error}`, ...prevMessages]);
            }
        };
        fetchCountries();
    }, []);

    const handleInputChange = (event) => {
      setNumberOfPersons(parseInt(event.target.value, 10) || 0);
    };

    const getRandomCountry = () => {
        if (availableCountries.length === 0) return "USA"; // Fallback if countries not loaded
        const randomIndex = Math.floor(Math.random() * availableCountries.length);
        return availableCountries[randomIndex].value;
    };

    const generateRandomPersons = async () => {
      const persons = [];
      for (let i = 0; i < numberOfPersons; i++) {
        persons.push({
          first_name: faker.person.firstName(),
          last_name: faker.person.lastName(),
          date_of_birth: faker.date.birthdate().toISOString().split('T')[0], // Format as YYYY-MM-DD
          email: faker.internet.email(),
          phone_number: faker.phone.number(),
          address: faker.location.streetAddress(),
          country: getRandomCountry()
        });
      }
      setGeneratedPersons(persons);

      // Send the generated persons to the backend API
      try {
          await axios.post('http://localhost:5000/api/persons', persons);
          setLogMessages((prevMessages) => [`${numberOfPersons} Persons successfully added to the database!`, ...prevMessages]);
          if (onGenerateComplete) onGenerateComplete(); // trigger refresh
      } catch (error) {
          alert('Failed to add persons to the database.');
          setLogMessages((prevMessages) => [`Error adding persons to the database: ${error}`, ...prevMessages]);
      }
    };

  return (
    <div>
      <h3>Generate Random Persons</h3>
      <input
        type="number"
        value={numberOfPersons}
        onChange={handleInputChange}
        placeholder="Enter number of persons"
      />
      <button onClick={generateRandomPersons}>Generate Persons</button>
    </div>
  );
};

export default PersonGenerator;
