import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './AnalyticsCard.css';

const AnalyticsCard = ({ personId }) => {
  const [analytics, setAnalytics] = useState({
    streaks: [],
    completionRates: [],
    consistency: 0,
    habitDistribution: {},
    habitCorrelations: []
  });

  const fetchAnalytics = async () => {
    try {
      const [streaksResponse, completionResponse, consistencyResponse, 
             distributionResponse, correlationsResponse] = await Promise.all([
        axios.get(`http://localhost:5000/api/analytics/persons/${personId}/streaks`),
        axios.get(`http://localhost:5000/api/analytics/persons/${personId}/completion-rates`),
        axios.get(`http://localhost:5000/api/analytics/persons/${personId}/consistency`),
        axios.get(`http://localhost:5000/api/analytics/persons/${personId}/distribution`),
        axios.get(`http://localhost:5000/api/analytics/persons/${personId}/correlations`)
      ]);

      setAnalytics({
        streaks: streaksResponse.data,
        completionRates: completionResponse.data,
        consistency: consistencyResponse.data.consistency_score,
        habitDistribution: distributionResponse.data,
        habitCorrelations: correlationsResponse.data
      });
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [personId]);

  return (
    <div className="analytics-card">
      <h4>Analytics</h4>
      
      <div className="analytics-section">
        <h5>Consistency Score</h5>
        <div className="consistency-score">
          {analytics.consistency.toFixed(2)}%
        </div>
      </div>

      <div className="analytics-section">
        <h5>Current Streaks</h5>
        {analytics.streaks.length > 0 ? (
          <ul>
            {analytics.streaks.map((streak) => (
              <li key={streak.habit_id}>
                {streak.habit_name}: {streak.current_streak} days
              </li>
            ))}
          </ul>
        ) : (
          <p>No active streaks</p>
        )}
      </div>

      <div className="analytics-section">
        <h5>Completion Rates</h5>
        {analytics.completionRates.length > 0 ? (
          <ul>
            {analytics.completionRates.map((rate) => (
              <li key={rate.habit_id}>
                {rate.habit_name}: {rate.completion_rate.toFixed(1)}%
              </li>
            ))}
          </ul>
        ) : (
          <p>No completion data</p>
        )}
      </div>

      <div className="analytics-section">
        <h5>Habit Distribution</h5>
        {Object.entries(analytics.habitDistribution).length > 0 ? (
          <ul>
            {Object.entries(analytics.habitDistribution).map(([category, count]) => (
              <li key={category}>
                {category}: {count} habits
              </li>
            ))}
          </ul>
        ) : (
          <p>No habit distribution data</p>
        )}
      </div>
    </div>
  );
};

export default AnalyticsCard; 