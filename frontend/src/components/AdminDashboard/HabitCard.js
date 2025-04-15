import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './HabitCard.css';

const HabitCard = ({ habit, personId, setLogMessages }) => {
  const [events, setEvents] = useState([]);

  const fetchHabitEvents = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/api/habits/${habit.habit_id}/events`);
      setEvents(res.data);
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
      fetchHabitEvents(); // ⤴️ Refresh
    } catch (error) {
      setLogMessages((prev) => [`Error creating event: ${error}`, ...prev]);
    }
  };

  useEffect(() => {
    fetchHabitEvents();
  }, []);

  return (
    <div className="habit-card">
      <div className="habit-card-header">
        <div>
          <div className="habit-name">{habit.name}</div>
          <div className="habit-category">{habit.category}</div>
        </div>
        <button className="add-event-button" onClick={handleCreateEvent}>+</button>
      </div>
      <div className="habit-events-row">
        {events.map((event) => (
          <div
            key={event.event_id}
            className="event-dot"
            title={new Date(event.timestamp).toLocaleString()}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default HabitCard;
