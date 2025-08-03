import React, { useEffect, useState } from 'react';
import axios from 'axios';
import HabitRow from './HabitRow';
import './PersonHabitDashboard.css';


const habitCategories = {
  "Health": ["Exercise", "Hydration", "Sleep", "Meditation", "Healthy Eating"],
  "Personal Development": ["Reading", "Learning a Skill", "Journaling", "Language Learning"],
  "Productivity": ["Time Management", "Planning", "Organization"],
  "Social": ["Connect with Friends", "Volunteering", "Networking"],
  "Financial": ["Saving Money", "Budgeting", "Investing"]
};



const useFetchPersons = (setLogMessages) => {
  const [persons, setPersons] = useState([]);

  const fetchPersons = async () => {
    try {
      console.log("Calling API:", `${process.env.REACT_APP_API_URL}/api/persons`);
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/persons`);
      setPersons(response.data);
    } catch (error) {
      setLogMessages((prevMessages) => [`Error fetching Persons:', ${error}`, ...prevMessages]);
    }
  };

  useEffect(() => {
    fetchPersons();
  }, []);

  return [persons, fetchPersons];
};

const useFetchHabits = (persons, setLogMessages) => {
  const [habits, setHabits] = useState({});

  const fetchHabits = async (personId) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/persons/${personId}/habits`);
      setHabits((prevHabits) => ({
        ...prevHabits,
        [personId]: response.data,
      }));
    } catch (error) {
      setLogMessages((prevMessages) => [`Error fetching habits for person ID ${personId}:`, error, ...prevMessages]);
    }
  };

  const fetchAllHabits = async () => {
    const updatedHabits = {};
    for (const person of persons) {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/persons/${person.person_id}/habits`);
      updatedHabits[person.person_id] = response.data;
    }
    setHabits(updatedHabits);
  };

  useEffect(() => {
    fetchAllHabits();
  }, [persons]);

  return [habits, fetchHabits, fetchAllHabits];
};

const useFetchHabitEvents = (habits, setLogMessages) => {
  const [habitEvents, setHabitEvents] = useState({});

  const fetchHabitEvents = async (habitId) => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/habits/${habitId}/events`);
        setHabitEvents((prevEvents) => ({
          ...prevEvents,
          [habitId]: response.data,
        }));
      } catch (error) {
        setLogMessages((prevMessages) => [`Error fetching habits for habit ID ${habitId}:`, error, ...prevMessages]);
      }
    };

    const fetchAllHabitEvents = async () => {
    const updatedEvents = {};
    for (const personId in habits) {
      for (const habit of habits[personId]) {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/habits/${habit.habit_id}/events`);
        updatedEvents[habit.habit_id] = response.data;
      }
    }
    setHabitEvents(updatedEvents);
    };

    useEffect(() => {
      fetchAllHabitEvents();
    }, [habits]);


  return [habitEvents, fetchHabitEvents, fetchAllHabitEvents];
};


const PersonHabitDashboard = ({ setLogMessages }) => {

  const [persons, fetchPersons] = useFetchPersons(setLogMessages);
  const [habits, fetchHabits, fetchAllHabits] = useFetchHabits(persons, setLogMessages);
  const [habitEvents, fetchHabitEvents, fetchAllHabitEvents] = useFetchHabitEvents(habits, setLogMessages);

  const createRandomHabit = async (personId) => {
    const categories = Object.keys(habitCategories);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    const habitsList = habitCategories[randomCategory];
    const randomHabit = habitsList[Math.floor(Math.random() * habitsList.length)];

    const newHabit = {
      person_id: personId,
      name: randomHabit,
      category: randomCategory,
      goal: "Daily",
    };

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/api/habits`, newHabit);
      
      setLogMessages((prevMessages) => [`Habit "${randomHabit}" created for person with ID ${personId}`, ...prevMessages]);

      fetchHabits(personId); // Refresh habits for the person
    } catch (error) {
      alert('Failed to create habit.');
      setLogMessages((prevMessages) => [`Error creating habit:, ${error}`, ...prevMessages]);
    }
  };

  const createHabitEvent = async (habitId, personId) => {
    const newEvent = {
      habit_id: habitId,
      person_id: personId,
      event_type: "Completion",
      timestamp: new Date().toISOString(),
      notes: "Completed habit for the day",
    };

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/api/habit_events`, newEvent);

      setLogMessages((prevMessages) => [`Habit event created for habit ID ${habitId}`, ...prevMessages]);

      fetchHabitEvents(habitId); // Refresh habit events for the habit
    } catch (error) {
      alert('Failed to create habit event.');
      setLogMessages((prevMessages) => [`Error creating habit event:', ${error}`, ...prevMessages]);
    }
  };

  return (
<div className="dashboard-container">
  <h2 className="dashboard-header">Person Habit Dashboard</h2>
  <button className="refresh-button" onClick={() => { fetchPersons(); fetchAllHabits(); fetchAllHabitEvents(); }}>Refresh List</button>
  <table className="dashboard-table">
    <thead>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Habit Name</th>
        <th>Category</th>
        <th>Actions</th>
        <th>Habit Events</th>
      </tr>
    </thead>
    <tbody>
      {persons.length > 0 ? (
        persons.map((person) => (
          <React.Fragment key={person.person_id}>
            <tr>
              <td className="tooltip" data-tooltip={JSON.stringify(person)}>
                {person.first_name}
              </td>
              <td>{person.last_name}</td>
              <td colSpan="4">
                <button className="action-button" onClick={() => createRandomHabit(person.person_id)}>
                  Create Random Habit
                </button>
              </td>
            </tr>
            {habits[person.person_id] && habits[person.person_id].length > 0 ? (
              habits[person.person_id].map((habit) => (
                <HabitRow
                  key={habit.habit_id}
                  habit={habit}
                  habitEvents={habitEvents[habit.habit_id] || []}
                  createHabitEvent={() => createHabitEvent(habit.habit_id, person.person_id)}
                />
              ))
            ) : (
              <tr>
                <td colSpan="6">No habits</td>
              </tr>
            )}
          </React.Fragment>
        ))
      ) : (
        <tr>
          <td colSpan="6">No persons found</td>
        </tr>
      )}
    </tbody>
  </table>
</div>

  );
};

export default PersonHabitDashboard;
