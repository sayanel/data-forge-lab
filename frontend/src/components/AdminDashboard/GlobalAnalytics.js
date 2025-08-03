import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './GlobalAnalytics.css';

const GlobalAnalytics = () => {
  const [analytics, setAnalytics] = useState({
    averageConsistency: 0,
    habitDistribution: {},
    categoryDistribution: {},
    habitPopularity: [],
    dropOffRates: {},
    firstWeekSuccess: {},
    engagement: {},
    geographicTrends: {},
    timeHeatmap: {}
  });

  const fetchGlobalAnalytics = async () => {
    try {
      const [consistencyResponse, distributionResponse, 
             categoryResponse, habitPopularityResponse,
             dropOffResponse, firstWeekResponse, engagementResponse, geoTrendsResponse, timeHeatmapResponse] = await Promise.all([
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/consistency`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/distribution`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/category-distribution`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/habit-popularity`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/drop-off-rates`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/first-week-success`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/engagement`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/geographic-trends`),
        axios.get(`${process.env.REACT_APP_API_URL}/api/analytics/time-heatmap`)
      ]);

      setAnalytics({
        averageConsistency: consistencyResponse.data.average_consistency,
        habitDistribution: distributionResponse.data,
        categoryDistribution: categoryResponse.data,
        habitPopularity: habitPopularityResponse.data || [],
        dropOffRates: dropOffResponse.data,
        firstWeekSuccess: firstWeekResponse.data,
        engagement: engagementResponse.data,
        geographicTrends: geoTrendsResponse.data,
        timeHeatmap: timeHeatmapResponse.data
      });
    } catch (error) {
      console.error('Error fetching global analytics:', error);
    }
  };

  useEffect(() => {
    fetchGlobalAnalytics();
  }, []);

  const maxCount = Math.max(...Object.values(analytics.timeHeatmap));

  return (
    <div className="global-analytics">
      <h3>Global Analytics</h3>
      
      <div className="analytics-grid">
        <div className="analytics-card">
          <h4>Average Consistency</h4>
          <div className="metric-value">
            {(analytics.averageConsistency ?? 0).toFixed(2)}%
          </div>
        </div>

        <div className="analytics-card">
          <h4>Habit Popularity</h4>
          <ul>
            {analytics.habitPopularity.map((habit, index) => (
              <li key={index}>
                {habit.habit_name}: {habit.user_count} users
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
          <h4>Drop-off Rates</h4>
          <ul>
            {Object.entries(analytics.dropOffRates).map(([habitId, data]) => (
              <li key={habitId}>{data.habit_name}: {data.drop_off_rate ? 'Dropped' : 'Active'} ({data.days_active} days)</li>
            ))}
          </ul>
        </div>
        <div className="analytics-card">
          <h4>First Week Success</h4>
          <ul>
            {Object.entries(analytics.firstWeekSuccess).map(([habitId, data]) => (
              <li key={habitId}>{data.habit_name}: {data.success_rate.toFixed(1)}%</li>
            ))}
          </ul>
        </div>
        <div className="analytics-card">
          <h4>Engagement Metrics</h4>
          <ul>
            <li>Daily Active Users: {analytics.engagement.active_users?.daily ?? 0}</li>
            <li>Weekly Active Users: {analytics.engagement.active_users?.weekly ?? 0}</li>
            <li>Monthly Active Users: {analytics.engagement.active_users?.monthly ?? 0}</li>
            <li>Avg Habits/User: {analytics.engagement.avg_habits_per_user?.toFixed(2) ?? 0}</li>
          </ul>
        </div>
        <div className="analytics-card">
          <h4>Geographic Trends</h4>
          <ul>
            {Object.entries(analytics.geographicTrends).map(([country, data]) => (
              <li key={country}>{country}: {data.total_habits} habits, {data.total_events} events, {data.active_users} active users</li>
            ))}
          </ul>
        </div>
        <div className="analytics-card">
          <h4>Time of Day Heatmap</h4>
          <div className="heatmap-row">
            {Object.entries(analytics.timeHeatmap).map(([hour, count]) => (
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
    </div>
  );
};

export default GlobalAnalytics; 