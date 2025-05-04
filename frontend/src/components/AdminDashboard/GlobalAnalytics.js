import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './GlobalAnalytics.css';

const GlobalAnalytics = () => {
  const [analytics, setAnalytics] = useState({
    averageConsistency: 0,
    habitDistribution: {},
    categoryDistribution: {},
    topHabits: [],
    correlationInsights: []
  });

  const fetchGlobalAnalytics = async () => {
    try {
      const [consistencyResponse, distributionResponse, 
             categoryResponse, topHabitsResponse, 
             correlationsResponse] = await Promise.all([
        axios.get('http://localhost:5000/api/analytics/global/consistency'),
        axios.get('http://localhost:5000/api/analytics/global/distribution'),
        axios.get('http://localhost:5000/api/analytics/global/category-distribution'),
        axios.get('http://localhost:5000/api/analytics/global/top-habits'),
        axios.get('http://localhost:5000/api/analytics/global/correlations')
      ]);

      setAnalytics({
        averageConsistency: consistencyResponse.data.average_consistency,
        habitDistribution: distributionResponse.data,
        categoryDistribution: categoryResponse.data,
        topHabits: topHabitsResponse.data,
        correlationInsights: correlationsResponse.data
      });
    } catch (error) {
      console.error('Error fetching global analytics:', error);
    }
  };

  useEffect(() => {
    fetchGlobalAnalytics();
  }, []);

  return (
    <div className="global-analytics">
      <h3>Global Analytics</h3>
      
      <div className="analytics-grid">
        <div className="analytics-card">
          <h4>Average Consistency</h4>
          <div className="metric-value">
            {analytics.averageConsistency.toFixed(2)}%
          </div>
        </div>

        <div className="analytics-card">
          <h4>Top Habits</h4>
          <ul>
            {analytics.topHabits.map((habit, index) => (
              <li key={index}>
                {habit.habit_name}: {habit.count} users
              </li>
            ))}
          </ul>
        </div>

        <div className="analytics-card">
          <h4>Category Distribution</h4>
          <ul>
            {Object.entries(analytics.categoryDistribution).map(([category, count]) => (
              <li key={category}>
                {category}: {count} habits
              </li>
            ))}
          </ul>
        </div>

        <div className="analytics-card">
          <h4>Habit Correlations</h4>
          <ul>
            {analytics.correlationInsights.map((insight, index) => (
              <li key={index}>
                {insight.habit1} ↔ {insight.habit2}: {insight.correlation.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default GlobalAnalytics; 