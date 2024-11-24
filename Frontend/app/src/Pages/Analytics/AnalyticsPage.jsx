import useAuth from "../../utils";
import React, { useState, useEffect } from 'react';
import { Line, Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './AnalyticsPage.css';

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const mockData = {
  totalApplications: 50,
  applicationDates: [
    '2017-08-21',
    '2018-05-30',
    '2019-01-14',
    '2020-03-07',
    '2021-11-11',
    '2022-08-14',
    '2023-06-18',
    '2023-12-05',
    '2024-02-11',
    '2024-03-21',
    '2024-04-30',
    '2024-05-23',
    '2024-06-10',
    '2024-07-15',
    '2024-08-19',
    '2024-08-26',
    '2024-09-02',
    '2024-09-09',
    '2024-09-16',
    '2024-09-23',
    '2024-09-30',
    '2024-10-05',
    '2024-10-06',
    '2024-10-07',
    '2024-10-08',
    '2024-10-09',
    '2024-10-10',
    '2024-10-11',
    '2024-10-12',
    '2024-10-13',
    '2024-10-14',
    '2024-10-15',
    '2024-10-16',
    '2024-10-17',
    '2024-10-18',
    '2024-10-19',
  ],
  applicationStatus: {
    'In progress': 10,
    'Awaiting Response': 20,
    'Interview(s) Scheduled': 15,
    'Awaiting Post-Interview Response': 10,
    Offer: 5,
    'Offer Accepted': 3,
    'Offer Declined': 2,
    Declined: 25,
    'No Response': 10,
  },
  timeToRespond: [
    3, 7, 14, 2, 10, 1, 5, 8, 12, 4,
    6, 9, 11, 13, 15, 20, 18, 17, 16, 19,
    14, 7, 3, 5, 2, 1, 4, 6, 13, 12,
    9, 8, 11, 10, 5, 7,
  ],
  applicationProgressionByLocation: {
    'San Francisco': {
      'No Response': 20,
      'Interview': 50,
      'Offer': 30,
    },
    'New York': {
      'No Response': 25,
      'Interview': 45,
      'Offer': 30,
    },
    'Seattle': {
      'No Response': 15,
      'Interview': 55,
      'Offer': 30,
    },
    'Austin': {
      'No Response': 10,
      'Interview': 60,
      'Offer': 30,
    },
    'Remote': {
      'No Response': 5,
      'Interview': 65,
      'Offer': 30,
    },
  },
  applicationProgressionByCompany: {
    'Google': {
      'No Response': 50,
      'Interview': 50,
      'Offer': 30,
    },
    'Amazon': {
      'No Response': 25,
      'Interview': 45,
      'Offer': 30,
    },
    'Facebook': {
      'No Response': 15,
      'Interview': 55,
      'Offer': 30,
    },
    'Microsoft': {
      'No Response': 10,
      'Interview': 60,
      'Offer': 30,
    },
    'Apple': {
      'No Response': 5,
      'Interview': 65,
      'Offer': 30,
    },
  },
  applicationProgressionByJobTitle: {
    'Software Engineer': {
      'No Response': 50,
      'Interview': 50,
      'Offer': 30,
    },
    'Software Developer': {
      'No Response': 25,
      'Interview': 45,
      'Offer': 30,
    },
    'Data Scientist': {
      'No Response': 15,
      'Interview': 55,
      'Offer': 30,
    },
    'Database Administrator': {
      'No Response': 10,
      'Interview': 60,
      'Offer': 30,
    },
    'Hardware Engineer': {
      'No Response': 5,
      'Interview': 65,
      'Offer': 30,
    },
  },
};

function Analytics() {

  const { authTokens } = useAuth();

  const [applications, setApplications] = useState([]);
  const [error, setError] = useState(null);

  // Fetch applications from the backend
  const fetchApplications = async () => {
    try {
      const response = await fetch("http://localhost:8000/application/get_applications", {
        headers: {
          Authorization: `Bearer ${authTokens}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setApplications(data); // Store the applications data
        // console.log("Fetched applications:", data);
      } else {
        throw new Error("Failed to fetch applications");
      }
    } catch (err) {
      setError("Error fetching applications");
      console.error("Error fetching applications:", err);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);


  const [timeFrame, setTimeFrame] = useState('week');

const totalApplications = applications.length;

// Use the current date in UTC
const today = new Date();
today.setUTCHours(0, 0, 0, 0);

// Function to get the Monday of the week for a given date in UTC
const getMonday = (d) => {
  const date = new Date(d);
  const day = date.getUTCDay();
  const diff = date.getUTCDate() - day + (day === 0 ? -6 : 1);
  const monday = new Date(date.setUTCDate(diff));
  monday.setUTCHours(0, 0, 0, 0);
  return monday;
};

// Function to format date keys consistently using UTC
const formatDateKey = (date) => {
  const year = date.getUTCFullYear();
  const month = ('0' + (date.getUTCMonth() + 1)).slice(-2);
  const day = ('0' + date.getUTCDate()).slice(-2);
  return `${year}-${month}-${day}`;
};

// Function to aggregate application dates based on the selected time frame
const getApplicationsOverTime = () => {
  // Since applied_date is now a Date object, we can use it directly
  const dates = applications.map((app) => new Date(app.applied_date));

  const aggregatedData = {};
  const labels = [];
  const dateKeys = [];

  if (timeFrame === 'day') {
    // Generate labels for the last 14 days ending today
    for (let i = 14; i >= 0; i--) {
      const date = new Date(today);
      date.setUTCDate(today.getUTCDate() - i);
      date.setUTCHours(0, 0, 0, 0);
      const key = formatDateKey(date);
      labels.push(
        date.toLocaleDateString('default', {
          weekday: 'long',
          month: '2-digit',
          day: '2-digit',
          timeZone: 'UTC', // Ensure UTC time zone is used
        })
      );
      dateKeys.push(key);
      aggregatedData[key] = 0;
    }
  } else if (timeFrame === 'week') {
    // Generate labels for the last 8 weeks ending with the current week
    const currentMonday = getMonday(today);
    for (let i = 7; i >= 0; i--) {
      const weekStart = new Date(currentMonday);
      weekStart.setUTCDate(currentMonday.getUTCDate() - i * 7);
      weekStart.setUTCHours(0, 0, 0, 0);
      const key = formatDateKey(weekStart);
      labels.push(
        weekStart.toLocaleDateString('default', {
          month: '2-digit',
          day: '2-digit',
          timeZone: 'UTC',
        })
      );
      dateKeys.push(key);
      aggregatedData[key] = 0;
    }
  } else if (timeFrame === 'month') {
    // Generate labels for the last 12 months ending with the current month
    for (let i = 11; i >= 0; i--) {
      const date = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth() - i, 1));
      date.setUTCHours(0, 0, 0, 0);
      const key = date.toLocaleString('default', {
        month: 'long',
        year: 'numeric',
        timeZone: 'UTC',
      });
      labels.push(key);
      dateKeys.push(key);
      aggregatedData[key] = 0;
    }
  } else if (timeFrame === 'year') {
    // Generate labels for the last 8 years ending with the current year
    for (let i = 7; i >= 0; i--) {
      const year = today.getUTCFullYear() - i;
      const key = year.toString();
      labels.push(key);
      dateKeys.push(key);
      aggregatedData[key] = 0;
    }
  }

  // Aggregate application dates into the labels
  dates.forEach((date) => {
    date.setUTCHours(0, 0, 0, 0);
    let key;

    if (timeFrame === 'day') {
      key = formatDateKey(date);
    } else if (timeFrame === 'week') {
      const monday = getMonday(date);
      key = formatDateKey(monday);
    } else if (timeFrame === 'month') {
      key = date.toLocaleString('default', {
        month: 'long',
        year: 'numeric',
        timeZone: 'UTC',
      });
    } else if (timeFrame === 'year') {
      key = date.getUTCFullYear().toString();
    }

    if (aggregatedData.hasOwnProperty(key)) {
      aggregatedData[key]++;
    }
  });

  // Get the counts in the order of labels
  const data = dateKeys.map((key) => aggregatedData[key]);

  return {
    labels,
    data,
  };
};

const applicationsOverTime = getApplicationsOverTime();

const applicationsOverTimeData = {
  labels: applicationsOverTime.labels,
  datasets: [
    {
      label: 'Applications Over Time',
      data: applicationsOverTime.data,
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      fill: false,
      tension: 0.1,
    },
  ],
};

const applicationsOverTimeOptions = {
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Number of Applications',
      },
    },
    x: {
      title: {
        display: true,
        text: 'Time Frame',
      },
    },
  },
};

  

  const handleTimeFrameChange = (event) => {
    setTimeFrame(event.target.value);
  };

  // Prepare data for the cumulative histogram
  const getCumulativeData = () => {
    const maxDays = 20;
    const daysArray = Array.from({ length: maxDays + 1 }, (_, i) => i);

    // Count applications responded at or before each day
    const cumulativeCounts = daysArray.map((day) => {
      return mockData.timeToRespond.filter((responseTime) => responseTime <= day).length;
    });

    return {
      labels: daysArray,
      data: cumulativeCounts,
    };
  };

  const cumulativeData = getCumulativeData();

  const cumulativeHistogramData = {
    labels: cumulativeData.labels,
    datasets: [
      {
        label: 'Cumulative Responses',
        data: cumulativeData.data,
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        fill: true,
        stepped: true,
      },
    ],
  };

  const cumulativeHistogramOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Days to Respond',
        },
        ticks: {
          precision: 0,
        },
      },
      y: {
        beginAtZero: true,
        min: 0,
        max: totalApplications,
        title: {
          display: true,
          text: 'Number of Applications',
        },
        ticks: {
          precision: 0,
          stepSize: Math.ceil(totalApplications / 10),
        },
      },
    },
  };

  // Generate unique colors
  const generateColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
      colors.push(`#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`);
    }
    return colors;
  };

  // Prepare application status data
  const statusCounts = applications.reduce((acc, { status }) => {
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {});

  const applicationStatusData = {
    labels: Object.keys(statusCounts),
    datasets: [
      {
        data: Object.values(statusCounts),
        backgroundColor: generateColors(Object.keys(statusCounts).length),
      },
    ],
  };

  const applicationStatusOptions = {
    plugins: {
      legend: {
        position: 'right',
      },
    },
  };

  // Function to assign colors to phases
  function getPhaseColor(phase) {
    const colors = {
      'No Response': 'rgba(255, 99, 132, 0.6)',
      'Interview': 'rgba(54, 162, 235, 0.6)',
      'Offer': 'rgba(75, 192, 192, 0.6)',
    };
    return colors[phase];
  }

const phases = ['No Response', 'Interview', 'Offer'];
const phaseChecker = ['Awaiting Response', 'Interview', 'Offer'];

// Utility function to process data for charts
const processDataForChart = (groupingAttribute, activePhases = phases) => {
  const uniqueValues = [...new Set(applications.map(app => app[groupingAttribute]))];

  const dataWithRatios = uniqueValues.map(value => {
    const groupedApps = applications.filter(app => app[groupingAttribute] === value);

    const phaseCounts = activePhases.map(() => 0);

    groupedApps.forEach(app => {
      let highestPhaseIndex = 0;
      if (Array.isArray(app.status_history)) {
        phaseChecker.forEach((checker, index) => {
          if (activePhases.includes(phases[index]) && app.status_history.includes(checker)) {
            highestPhaseIndex = index;
          }
        });
      }
      phaseCounts[highestPhaseIndex]++;
    });

    const total = groupedApps.length;
    const percentages = phaseCounts.map(count => (count / total) * 100);

    return {
      value,
      percentages,
    };
  });

  dataWithRatios.sort((a, b) => {
    for (let i = activePhases.length - 1; i >= 0; i--) {
      const diff = b.percentages[i] - a.percentages[i];
      if (diff !== 0) return diff;
    }
    return 0;
  });

  return {
    labels: dataWithRatios.map(item => item.value),
    datasets: activePhases.map((phase, phaseIndex) => ({
      label: phase,
      data: dataWithRatios.map(item => item.percentages[phaseIndex].toFixed(2)),
      backgroundColor: getPhaseColor(phase),
    })),
  };
};

// Configure the data for each chart

const progressionByLocationData = processDataForChart('location');
const progressionByJobTitleData = processDataForChart('position');
const progressionByCompanyData = processDataForChart('company');

// Options remain the same for all charts
const progressionOptions = {
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: (value) => `${value}%`,
      },
      title: {
        display: true,
        text: 'Percentage of Applications (%)',
      },
      stacked: true,
    },
    x: {
      title: {
        display: true,
        text: 'Attribute',
      },
      stacked: true,
    },
  },
  plugins: {
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.dataset.label || '';
          const value = context.parsed.y || 0;
          return `${label}: ${value}%`;
        },
      },
    },
    legend: {
      position: 'top',
    },
  },
};

const progressionOptionsLocation = {
  ...progressionOptions,
  scales: {
    ...progressionOptions.scales,
    x: {
      ...progressionOptions.scales.x,
      title: {
        ...progressionOptions.scales.x.title,
        text: 'Locations',
      },
    },
  },
};

const progressionOptionsCompany = {
  ...progressionOptions,
  scales: {
    ...progressionOptions.scales,
    x: {
      ...progressionOptions.scales.x,
      title: {
        ...progressionOptions.scales.x.title,
        text: 'Companies',
      },
    },
  },
};

const progressionOptionsJobTitle = {
  ...progressionOptions,
  scales: {
    ...progressionOptions.scales,
    x: {
      ...progressionOptions.scales.x,
      title: {
        ...progressionOptions.scales.x.title,
        text: 'Job Titles',
      },
    },
  },
};

  const getNewEmails = async () => {
    try {
      if (!LastUpdateTime) {
        await getAllEmails(); // Fetch all emails if no update time is set
      } else {
        const response = await fetch(
          `http://localhost:8000/outlook_api/get-user-messages-by-phrase-and-date?phrase=applying&last_refresh_time=${LastUpdateTime}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${authTokens}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();

          if (data.message === "No new emails found") {
            setError("No new emails found");
            return;
          }

          // Iterate over each email and create or update an application
          for (const email of data) {
            const companyName = email.company || "";
            const existingApplication = applications.find(
              (app) => app.company === companyName
            );

            // Prepare formData for the application
            const formData = {
              company: companyName,
              position: email.position || "",
              location: email.location || "",
              status: email.status || "",
              applied_date: email.receivedDateTime || "",
              last_update: email.receivedDateTime || "",
              salary: email.salary || "",
              job_description: email.job_description || "",
              notes: email.notes || "",
              status_history: email.status_history || {},
              interview_notes: email.interview_notes || "",
              interview_dates: email.interview_dates || "",
              interview_round: email.interview_round || "",
              is_active_interview: email.is_active_interview || false,
              offer_notes: email.offer_notes || "",
              offer_interest: email.offer_interest || 0,
              is_active_offer: email.is_active_offer || false,
            };

            if (existingApplication) {
              // Update the existing application status
              await handleSubmit(existingApplication.id, formData);
            } else {
              // Create a new application
              await handleCreate(formData);
            }

            // Create the email object and associate it with the application
            await createEmailObject(email, existingApplication ? existingApplication.id : null);
          }

          updateLastUpdateTime(); // Only update after successful fetch
        } else {
          throw new Error("Failed to get new emails");
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // Function to create an email object
  const createEmailObject = async (email, applicationId) => {
    const emailData = {
      app: applicationId, // Link to the application if it exists
      user_id: authTokens.userId, // Assuming you have user ID in authTokens
      subject: email.subject || "",
      sender: email.sender || "",
      received_date: email.receivedDateTime || "",
      body: email.body || "",
      body_preview: email.bodyPreview || "",
      status: email.status || "",
    };

    try {
      const response = await fetch(
        "http://localhost:8000/email/create_email", // Adjust the endpoint as necessary
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify(emailData),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create email object");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="analytics-page">
      <h2>Application Analytics</h2>

      <section className="analytics-section">
        <h2>Total Applications: {totalApplications}</h2>
      </section>

      <section className="analytics-section">
        <h2>Applications Over Time</h2>

        <div className="timeframe-selector">
          <label>Select Time Frame: </label>
          <select value={timeFrame} onChange={handleTimeFrameChange}>
            <option value="day">Day</option>
            <option value="week">Week</option>
            <option value="month">Month</option>
            <option value="year">Year</option>
          </select>
        </div>

        <div className="chart-container">
          <Line data={applicationsOverTimeData} options={applicationsOverTimeOptions} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Status</h2>
        <div className="chart-container">
          <Pie data={applicationStatusData} options={applicationStatusOptions} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Cumulative Time to Respond</h2>
        <div className="chart-container">
          <Line data={cumulativeHistogramData} options={cumulativeHistogramOptions} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Progression vs Location</h2>
        <div className="chart-container">
          <Bar data={progressionByLocationData} options={progressionOptionsLocation} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Progression vs Company</h2>
        <div className="chart-container">
          <Bar data={progressionByCompanyData} options={progressionOptionsCompany} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Progression vs Job Title</h2>
        <div className="chart-container">
          <Bar data={progressionByJobTitleData} options={progressionOptionsJobTitle} />
        </div>
      </section>
    </div>
  );
}

export default Analytics;