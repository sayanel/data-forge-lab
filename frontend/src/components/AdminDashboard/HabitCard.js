import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './HabitCard.css';

const HabitCard = ({ habit, personId, setLogMessages, onEventCreated, onDeleteHabit, currentStreak }) => {
  const [events, setEvents] = useState([]);

  const fetchHabitEvents = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/api/habits/${habit.habit_id}/events`);
      setEvents(res.data);
      setLogMessages((prev) => [`Fetched ${res.data.length} events for habit "${habit.name}"`, ...prev]);
    } catch (error) {
      setLogMessages((prev) => [`Error fetching events: ${error}`, ...prev]);
    }
  };

  const handleCreateEvent = async () => {
    const newEvent = {
      habit_id: habit.habit_id,
      person_id: personId,
      timestamp: new Date().toISOString(),
      notes: "Completed habit",
      status: "completed"
    };

    try {
      await axios.post('http://localhost:5000/api/habit_events', newEvent);
      setLogMessages((prev) => [`Event created for habit "${habit.name}"`, ...prev]);
      await fetchHabitEvents();
      if (onEventCreated) {
        onEventCreated();
        setLogMessages((prev) => [`Refreshing habit card for "${habit.name}"`, ...prev]);
      }
    } catch (error) {
      setLogMessages((prev) => [`Error creating event: ${error}`, ...prev]);
    }
  };

  const handleDeleteHabit = () => {
    if (onDeleteHabit) {
      onDeleteHabit(habit.habit_id);
    }
  };

  useEffect(() => {
    fetchHabitEvents();
  }, [habit.habit_id]);

  return (
    <div
      className="habit-card"
      title={`Name: ${habit.name}\nGoal: ${habit.goal}\nCategory: ${habit.category}\nHabit ID: ${habit.habit_id}\nCreated At: ${habit.created_at}\nUpdated At: ${habit.updated_at || 'N/A'}\nStreak: ${habit.streak}\nLast Completed: ${habit.last_completed || 'N/A'}`}
    >
      <div className="habit-card-header">
        <div>
          <div className="habit-name">{habit.name}</div>
          <div className="habit-category">{habit.category}</div>
        </div>
        <div className="habit-card-header-buttons">
          <div className="streak-circle" title="Current streak">{currentStreak}</div>
          <button className="add-event-button" onClick={handleCreateEvent}>+</button>
          <button className="delete-habit-button" onClick={handleDeleteHabit}>-</button>
        </div>
      </div>
      <div className="habit-events-row">
        {events.map((event, idx) => (
          <div
            key={event.event_id || event._id || idx}
            className="event-dot"
            title={`Event ID: ${event.event_id || event._id || idx}\nPerson ID: ${event.person_id}\nHabit ID: ${event.habit_id}\nTimestamp: ${event.timestamp}\nNotes: ${event.notes || ''}\nStatus: ${event.status}`}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default HabitCard;
