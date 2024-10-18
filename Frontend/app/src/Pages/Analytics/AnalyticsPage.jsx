import React from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
import './AnalyticsPage.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

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
  topCompanies: {
    'Google': 30,
    'Facebook': 20,
    'Amazon': 15,
    'Microsoft': 10,
    'Apple': 5,
  },
  resumeVersions: {
    'Version 1': 0.6,
    'Version 2': 0.8,
    'Version 3': 0.7,
  },
  applicationTimeline: {
    'January': 10,
    'February': 20,
    'March': 30,
    'April': 40,
  },
  applicationSuccessRateByJobTitle: {
    'Software Engineer': {
      'Version 1': 0.5,
      'Version 2': 0.6,
      'Version 3': 0.4,
    },
    'Data Scientist': {
      'Version 1': 0.3,
      'Version 2': 0.4,
      'Version 3': 0.5,
    },
    'Product Manager': {
      'Version 1': 0.2,
      'Version 2': 0.3,
      'Version 3': 0.4,
    },
  },
  applicationSuccessRateByLocation: {
    'San Francisco': {
      'Version 1': 0.4,
      'Version 2': 0.5,
      'Version 3': 0.6,
    },
    'New York': {
      'Version 1': 0.3,
      'Version 2': 0.4,
      'Version 3': 0.5,
    },
    'Seattle': {
      'Version 1': 0.2,
      'Version 2': 0.3,
      'Version 3': 0.4,
    },
  },
  averageTimeToResponse: {
    'Google': 10,
    'Facebook': 15,
    'Amazon': 20,
    'Microsoft': 25,
    'Apple': 30,
  },
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

  const topCompaniesData = {
    labels: Object.keys(mockData.topCompanies),
    datasets: [
      {
        label: 'Applications',
        data: Object.values(mockData.topCompanies),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      },
    ],
  };

  const resumeVersionsData = {
    labels: Object.keys(mockData.resumeVersions),
    datasets: [
      {
        label: 'Success Rate',
        data: Object.values(mockData.resumeVersions),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56'
        ],
      },
    ],
  };

  const applicationTimelineData = {
    labels: Object.keys(mockData.applicationTimeline),
    datasets: [
      {
        label: 'Applications Over Time',
        data: Object.values(mockData.applicationTimeline),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false,
      },
    ],
  };

  const applicationSuccessRateByJobTitleData = {
    labels: Object.keys(mockData.applicationSuccessRateByJobTitle),
    datasets: Object.keys(mockData.resumeVersions).map((version, index) => ({
      label: `Success Rate by Job Title (${version})`,
      data: Object.values(mockData.applicationSuccessRateByJobTitle).map(jobTitleData => jobTitleData[version]),
      backgroundColor: `rgba(${index * 50}, ${index * 100}, ${index * 150}, 0.6)`,
    })),
  };

  const applicationSuccessRateByLocationData = {
    labels: Object.keys(mockData.applicationSuccessRateByLocation),
    datasets: Object.keys(mockData.resumeVersions).map((version, index) => ({
      label: `Success Rate by Location (${version})`,
      data: Object.values(mockData.applicationSuccessRateByLocation).map(locationData => locationData[version]),
      backgroundColor: `rgba(${index * 50}, ${index * 100}, ${index * 150}, 0.6)`,
    })),
  };

  const averageTimeToResponseData = {
    labels: Object.keys(mockData.averageTimeToResponse),
    datasets: [
      {
        label: 'Average Time to Response (days)',
        data: Object.values(mockData.averageTimeToResponse),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
      },
    ],
  };

  return (
    <div className="analytics-page">
      <h2>Application Analytics</h2>
      
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
        <h2>Top Companies Applied To</h2>
        <div className="chart-container">
          <Bar data={topCompaniesData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Resume Versions Success Rate</h2>
        <div className="chart-container">
          <Pie data={resumeVersionsData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Timeline</h2>
        <div className="chart-container">
          <Line data={applicationTimelineData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Success Rate by Job Title</h2>
        <div className="chart-container">
          <Bar data={applicationSuccessRateByJobTitleData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Success Rate by Location</h2>
        <div className="chart-container">
          <Bar data={applicationSuccessRateByLocationData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Average Time to Response</h2>
        <div className="chart-container">
          <Bar data={averageTimeToResponseData} />
        </div>
      </section>

      {/* Add more sections for other important statistics */}
    </div>
  );
}

export default Analytics;