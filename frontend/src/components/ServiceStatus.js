import React, { useEffect, useState } from 'react';
import axios from 'axios';

const statusLabels = {
  mongo: 'MongoDB',
  kafka: 'Kafka',
  flask: 'Flask (API)'
};

const dotStyle = (ok) => ({
  display: 'inline-block',
  width: 14,
  height: 14,
  borderRadius: '50%',
  background: ok ? '#4caf50' : '#f44336',
  marginRight: 8,
  border: '1px solid #888',
});

const ServiceStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/system/status`);
        setStatus(res.data);
      } catch (e) {
        setStatus({ mongo: false, kafka: false, flask: false });
      } finally {
        setLoading(false);
      }
    };
    fetchStatus();
  }, []);

  return (
    <div style={{ padding: 16, borderRadius: 8, background: '#f7f7f7', marginBottom: 24 }}>
      <h4 style={{ margin: '0 0 12px 0' }}>Service Status</h4>
      {loading ? (
        <div>Checking...</div>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {Object.keys(statusLabels).map((key) => (
            <li key={key} style={{ display: 'flex', alignItems: 'center', marginBottom: 6 }}>
              <span style={dotStyle(status && status[key])}></span>
              <span>{statusLabels[key]}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ServiceStatus; 