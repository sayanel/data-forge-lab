import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PersonCard.css';
import HabitCard from './HabitCard';
import AnalyticsCard from './AnalyticsCard';


const habitCategories = {
  "Health": ["Exercise", "Hydration", "Sleep", "Meditation", "Healthy Eating"],
  "Personal Development": ["Reading", "Learning a Skill", "Journaling", "Language Learning"],
  "Productivity": ["Time Management", "Planning", "Organization"],
  "Social": ["Connect with Friends", "Volunteering", "Networking"],
  "Financial": ["Saving Money", "Budgeting", "Investing"]
};

const PersonCard = ({ person, setLogMessages }) => {
  const [habits, setHabits] = useState([]);

  const fetchHabits = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/persons/${person.person_id}/habits`);
      setHabits(response.data);
      setLogMessages((prev) => [`Fetched ${response.data.length} habits for ${person.first_name}`, ...prev]);
    } catch (error) {
      setLogMessages((prev) => [`Error fetching habits: ${error}`, ...prev]);
    }
  };

  const createRandomHabit = async () => {
    const categories = Object.keys(habitCategories);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    const habitsList = habitCategories[randomCategory];
    const randomHabit = habitsList[Math.floor(Math.random() * habitsList.length)];

    const newHabit = {
      person_id: person.person_id,
      name: randomHabit,
      category: randomCategory,
      goal: "Daily"
    };

    try {
      await axios.post('http://localhost:5000/api/habits', newHabit);
      setLogMessages((prev) => [`Habit "${randomHabit}" created for ${person.first_name}`, ...prev]);
      await fetchHabits(); // refresh after creation
    } catch (error) {
      setLogMessages((prev) => [`Error creating habit: ${error}`, ...prev]);
    }
  };

  const handleEventCreated = async () => {
    setLogMessages((prev) => [`Refreshing habits for ${person.first_name} after event creation`, ...prev]);
    await fetchHabits();
  };

  const handleDeleteHabit = async (habitId) => {
    try {
      await axios.delete(`http://localhost:5000/api/habits/${habitId}`);
      setLogMessages((prev) => [`Habit deleted`, ...prev]);
      await fetchHabits();
    } catch (error) {
      setLogMessages((prev) => [`Error deleting habit: ${error}`, ...prev]);
    }
  };

  // Fetch habits when the card mounts
  useEffect(() => {
    fetchHabits();
  }, []);

  return (
    <div className="person-card">
      <h3>{person.first_name} {person.last_name}</h3>
      <p><strong>ID:</strong> {person.person_id}</p>
      <p><strong>Email:</strong> {person.email || "N/A"}</p>

      <button className="create-habit-button" onClick={createRandomHabit}>
        Create Random Habit
      </button>

      <div className="habit-section">
          <h4>Habits</h4>
          {habits.length > 0 ? (
            habits.map((habit) => (
              <HabitCard
                key={habit.habit_id}
                habit={habit}
                personId={person.person_id}
                setLogMessages={setLogMessages}
                onEventCreated={handleEventCreated}
                onDeleteHabit={handleDeleteHabit}
              />
            ))
          ) : (
            <p>No habits found.</p>
          )}
      </div>

      <AnalyticsCard personId={person.person_id} />
    </div>
  );
};

export default PersonCard;
