import React, { useState } from 'react';
import axios from 'axios';

const CreateHabit = () => {
  const [formData, setFormData] = useState({
    name: '',
    goal: '',
    category: '',
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/habits', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 201) {
        setMessage('Habit created successfully!');
        setFormData({ name: '', goal: '', category: '' });
      } else {
        setMessage('Failed to create habit. Please try again..');
      }

    } catch (error) {
      setMessage('Failed to create habit. Please try again.');
      console.error('Error creating habit:', error);
    }
  };

  return (
    <div>
      <h2>Create a New Habit</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Habit Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="goal">Goal:</label>
          <input
            type="text"
            id="goal"
            name="goal"
            value={formData.goal}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="category">Category:</label>
          <input
            type="text"
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Create Habit</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default CreateHabit;
