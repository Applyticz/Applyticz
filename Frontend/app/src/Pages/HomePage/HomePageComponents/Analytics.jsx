import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './Analytics.css';  // Add this line


ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// Mock data - replace with actual data from your backend
const mockData = {
  totalApplications: 100,
  statusTotals: {
    Applied: 50,
    'Further Review': 20,
    'Interview Scheduled': 15,
    Interviewed: 10,
    Rejected: 3,
    Accepted: 1,
    Declined: 1,
  },
  resumeSuccessRate: 0.75,
  locationSuccessRate: 0.8,
  jobTitleSuccessRate: 0.7,
};

function Analytics() {
  const statusData = {
    labels: Object.keys(mockData.statusTotals),
    datasets: [
      {
        data: Object.values(mockData.statusTotals),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384'
        ],
      },
    ],
  };

  const successRatesData = {
    labels: ['Resume', 'Location', 'Job Title'],
    datasets: [
      {
        label: 'Success Rate',
        data: [
          mockData.resumeSuccessRate,
          mockData.locationSuccessRate,
          mockData.jobTitleSuccessRate,
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  return (
    <div className="analytics-page">
      <h1>Application Analytics</h1>
      
      <section className="analytics-section">
        <h2>Total Applications: {mockData.totalApplications}</h2>
      </section>

      <section className="analytics-section">
        <h2>Application Status</h2>
        <div className="chart-container">
          <Pie data={statusData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Success Rates</h2>
        <div className="chart-container">
          <Bar 
            data={successRatesData}
            options={{
              scales: {
                y: {
                  beginAtZero: true,
                  max: 1,
                  ticks: {
                    callback: (value) => `${Number(value) * 100}%`,
                  },
                },
              },
            }}
          />
        </div>
      </section>

      {/* Add more sections for other important statistics */}
    </div>
  );
}

export default Analytics;