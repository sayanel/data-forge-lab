import React from 'react';
import './Log.css'; // Create a CSS file for styling

const Log = ({ messages }) => {

  const formatMessageWithTimestamp = (message) => {
    const timestamp = new Date().toTimeString().split(' ')[0];
    const formattedMessage = `${timestamp} - ${message}`;
    console.log(formattedMessage);
    return formattedMessage;
  };

  return (
    <div className="log-container">
      {messages.map((message, index) => (
        <div key={index} className="log-message">
          {formatMessageWithTimestamp(message)}
        </div>
      ))}
    </div>
  );
};

export default Log;
