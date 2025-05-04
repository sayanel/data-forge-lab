import React from 'react';

const HabitRow = ({ habit, habitEvents, createHabitEvent }) => {
  return (
    <tr>
      <td colSpan="2"></td>
      <td>{habit.name}</td>
      <td>{habit.category}</td>
      <td>
        <button className="action-button" onClick={() => createHabitEvent(habit.habit_id, habit.person_id)}>
          Create Habit Event
        </button>
      </td>
      <td>
        {habitEvents.length > 0 ? (
          habitEvents.map((event, index) => (
            <div key={index} title={JSON.stringify(event)} style={{ cursor: 'pointer', margin: '2px 0' }}>
              {event.event_type} ({new Date(event.timestamp).toLocaleString()})
            </div>
          ))
        ) : (
          'No events'
        )}
      </td>
    </tr>
  );
};

export default HabitRow;
