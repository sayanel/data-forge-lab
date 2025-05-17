import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './AnalyticsCard.css';

const AnalyticsCard = ({ personId }) => {
  const [analytics, setAnalytics] = useState({
    streaks: [],
    completionRates: [],
    consistency: 0,
    habitDistribution: {},
    habitCorrelations: [],
    timeHeatmap: {}
  });

  const fetchAnalytics = async () => {
    try {
      const [completionResponse, consistencyResponse, distributionResponse, heatmapResponse] = await Promise.all([
        axios.get(`http://localhost:5000/api/analytics/completion-rates?person_id=${personId}`),
        axios.get(`http://localhost:5000/api/analytics/consistency?person_id=${personId}`),
        axios.get(`http://localhost:5000/api/analytics/distribution?person_id=${personId}`),
        axios.get(`http://localhost:5000/api/analytics/time-heatmap?person_id=${personId}`)
      ]);

      setAnalytics({
        completionRates: completionResponse.data,
        consistency: consistencyResponse.data.consistency,
        habitDistribution: distributionResponse.data,
        timeHeatmap: heatmapResponse.data
      });
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [personId]);

  const maxCount = Math.max(...Object.values(analytics.timeHeatmap || {}));

  return (
    <div className="analytics-card">
      <h4>Analytics</h4>
      
      <div className="analytics-section">
        <h5>Consistency Score</h5>
        <div className="consistency-score">
          {(analytics.consistency ?? 0).toFixed(2)}%
        </div>
      </div>

      <div className="analytics-section">
        <h5>Completion Rates</h5>
        {analytics.completionRates.length > 0 ? (
          <ul>
            {analytics.completionRates.map((rate) => (
              <li key={rate.habit_id}>
                {rate.habit_name}: {(rate.completion_rate ?? 0).toFixed(1)}%
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

      <div className="analytics-section">
        <h5>Time of Day Heatmap</h5>
        <div className="heatmap-row">
          {analytics.timeHeatmap && Object.entries(analytics.timeHeatmap).map(([hour, count]) => (
            <div
              key={hour}
              className="heatmap-cell"
              title={`${hour}: ${count}`}
              style={{
                background: `rgba(33, 150, 243, ${Math.min(count / maxCount, 1) || 0.1})`,
                color: count > (maxCount * 0.5) ? '#fff' : '#222'
              }}
            >
              <span className="heatmap-hour">{hour}</span>
              <span className="heatmap-count">{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsCard; 