import React, { useEffect, useState } from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
import useAuth from "../../utils";
import './AnalyticsPage.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

function Analytics() {
  const { authTokens } = useAuth();
  const [applicationData, setApplicationData] = useState(null); // Store the real data
  const [loading, setLoading] = useState(true); // Handle loading state
  const [errorMessage, setErrorMessage] = useState(""); // Store error messages if any
  const [theme, setTheme] = useState('light');
  const [error, setError] = useState('');

  // Fetch the theme from the backend
  const fetchTheme = async () => {
    try {
      const response = await fetch("http://localhost:8000/settings/get_settings", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Theme response:", data.theme);
        setTheme(data.theme || 'light');
      } else {
        throw new Error('Failed to fetch theme');
      }
    } catch (err) {
      console.log('Error fetching theme:', err);
      setError('Error fetching theme');
    }
  };

  useEffect(() => {
    // Apply the theme by toggling class on the root element
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
  }, [theme]);

  useEffect(() => { fetchTheme(); }, []);

  // Fetch application data from the backend
  const getApplicationData = async () => {
    try {
      const response = await fetch("http://localhost:8000/application/get_applications", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setApplicationData(data); // Set the real data
        console.log("Application data:", data);
        setLoading(false); // Stop loading
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch applications");
        setLoading(false);
      }
    } catch (error) {
      setErrorMessage("Error fetching applications");
      console.error("Error fetching applications:", error);
      setLoading(false);
    }
  };

  // Process data for the charts (based on the structure of your real data)
  const processData = (data) => {
    const statusTotals = data.reduce((acc, app) => {
      const status = app.status;
      acc[status] = (acc[status] || 0) + 1;
      return acc;
    }, {});

    const topCompanies = data.reduce((acc, app) => {
      const company = app.company;
      acc[company] = (acc[company] || 0) + 1;
      return acc;
    }, {});

    // New analytics: Applications over time
    const applicationsOverTime = data.reduce((acc, app) => {
      const date = new Date(app.date_applied).toLocaleDateString();
      acc[date] = (acc[date] || 0) + 1;
      return acc;
    }, {});

    // New analytics: Success rate by company
    const successRateByCompany = data.reduce((acc, app) => {
      const company = app.company;
      if (!acc[company]) {
        acc[company] = { total: 0, successful: 0 };
      }
      acc[company].total += 1;
      if (app.status === 'Accepted') {
        acc[company].successful += 1;
      }
      return acc;
    }, {});

    // Calculate success rates
    for (const company in successRateByCompany) {
      const { total, successful } = successRateByCompany[company];
      successRateByCompany[company] = (successful / total) * 100;
    }

    // Return processed data for all charts
    return {
      statusTotals,
      topCompanies,
      applicationsOverTime,
      successRateByCompany,
      // Other processed data
    };
  };

  // Fetch the data on component mount
  useEffect(() => {
    getApplicationData();
  }, []);

  // If data is still loading, show a loading message
  if (loading) {
    return <div>Loading...</div>;
  }

  // If there's an error, show the error message
  if (errorMessage) {
    return <div>Error: {errorMessage}</div>;
  }

  // If no data is available, return a message
  if (!applicationData) {
    return <div>No data available</div>;
  }

  // Process the application data for the charts
  const processedData = processData(applicationData);

  const statusData = {
    labels: Object.keys(processedData.statusTotals),
    datasets: [
      {
        data: Object.values(processedData.statusTotals),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384'],
      },
    ],
  };

  const topCompaniesData = {
    labels: Object.keys(processedData.topCompanies),
    datasets: [
      {
        label: 'Applications',
        data: Object.values(processedData.topCompanies),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      },
    ],
  };

  const applicationsOverTimeData = {
    labels: Object.keys(processedData.applicationsOverTime),
    datasets: [
      {
        label: 'Applications Over Time',
        data: Object.values(processedData.applicationsOverTime),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  const successRateByCompanyData = {
    labels: Object.keys(processedData.successRateByCompany),
    datasets: [
      {
        label: 'Success Rate (%)',
        data: Object.values(processedData.successRateByCompany),
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
      },
    ],
  };

  // Return the JSX with real data
  return (
    <div className="analytics-page">
      <h2>Application Analytics</h2>

      <section className="analytics-section">
        <h2>Total Applications: {applicationData.length}</h2>
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
        <h2>Applications Over Time</h2>
        <div className="chart-container">
          <Line data={applicationsOverTimeData} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Success Rate by Company</h2>
        <div className="chart-container">
          <Bar data={successRateByCompanyData} />
        </div>
      </section>

      {/* Add more charts with processedData as needed */}
    </div>
  );
}

export default Analytics;
