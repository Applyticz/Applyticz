import React, { useState } from 'react';
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

  const [timeFrame, setTimeFrame] = useState('week');

  const phases = ['No Response', 'Interview', 'Offer'];
  
  const totalApplications = mockData.totalApplications;

  // Use the current date
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Function to get the Monday of the week for a given date
  const getMonday = (d) => {
    const date = new Date(d);
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    const monday = new Date(date.setDate(diff));
    monday.setHours(0, 0, 0, 0); 
    return monday;
  };

  // Function to format date keys consistently
  const formatDateKey = (date) => {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    return `${year}-${month}-${day}`;
  };

  // Function to aggregate application dates based on the selected time frame
  const getApplicationsOverTime = () => {
    const { applicationDates } = mockData;

    // Parse the date strings to Date objects
    const dates = applicationDates.map((dateStr) => {
      const [year, month, day] = dateStr.split('-').map(Number);
      return new Date(year, month - 1, day);
    });

    const aggregatedData = {};
    const labels = [];
    const dateKeys = [];

    if (timeFrame === 'day') {
      // Generate labels for the last 14 days ending today
      for (let i = 14; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        date.setHours(0, 0, 0, 0);
        const key = formatDateKey(date);
        labels.push(
          date.toLocaleDateString('default', {
            weekday: 'long',
            month: '2-digit',
            day: '2-digit',
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
        weekStart.setDate(currentMonday.getDate() - i * 7);
        weekStart.setHours(0, 0, 0, 0);
        const key = formatDateKey(weekStart);
        labels.push(
          weekStart.toLocaleDateString('default', {
            month: '2-digit',
            day: '2-digit',
          })
        );
        dateKeys.push(key);
        aggregatedData[key] = 0;
      }
    } else if (timeFrame === 'month') {
      // Generate labels for the last 12 months ending with the current month
      for (let i = 11; i >= 0; i--) {
        const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
        date.setHours(0, 0, 0, 0);
        const key = date.toLocaleString('default', {
          month: 'long',
          year: 'numeric',
        });
        labels.push(key);
        dateKeys.push(key);
        aggregatedData[key] = 0;
      }
    } else if (timeFrame === 'year') {
      // Generate labels for the last 8 years ending with the current year
      for (let i = 7; i >= 0; i--) {
        const year = today.getFullYear() - i;
        const key = year.toString();
        labels.push(key);
        dateKeys.push(key);
        aggregatedData[key] = 0;
      }
    }

    // Aggregate application dates into the labels
    dates.forEach((date) => {
      date.setHours(0, 0, 0, 0);
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
        });
      } else if (timeFrame === 'year') {
        key = date.getFullYear().toString();
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

  const applicationStatusData = {
    labels: Object.keys(mockData.applicationStatus),
    datasets: [
      {
        data: Object.values(mockData.applicationStatus),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#8A2BE2',
          '#FF1493',
          '#00CED1',
        ],
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

  //Prepare data for the stacked bar chart (Application Progression vs Location)
  const progressionByLocationData = {
    labels: Object.keys(mockData.applicationProgressionByLocation),
    datasets: phases.map((phase) => ({
      label: phase,
      data: Object.values(mockData.applicationProgressionByLocation).map(
        (locationData) => {
          const total = Object.values(locationData).reduce(
            (sum, count) => sum + count,
            0
          );
          const phaseCount = locationData[phase] || 0;
          const percentage = (phaseCount / total) * 100;
          return percentage.toFixed(2);
        }
      ),
      backgroundColor: getPhaseColor(phase),
    })),
  };

  const progressionByLocationOptions = {
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
          text: 'Location',
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

  // repare data for the stacked bar chart (Application Progression vs Company)
  const progressionByCompanyData  = {
    labels: Object.keys(mockData.applicationProgressionByCompany),
    datasets: phases.map((phase) => ({
      label: phase,
      data: Object.values(mockData.applicationProgressionByCompany).map(
        (companyData) => {
          const total = Object.values(companyData).reduce(
            (sum, count) => sum + count,
            0
          );
          const phaseCount = companyData[phase] || 0;
          const percentage = (phaseCount / total) * 100;
          return percentage.toFixed(2);
        }
      ),
      backgroundColor: getPhaseColor(phase),
    })),
  };

  const progressionByCompanyOptions = {
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
          text: 'Company',
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

  // Prepare data for the stacked bar chart (Application Progression vs Job Title)
  const progressionByJobTitleData  = {
    labels: Object.keys(mockData.applicationProgressionByJobTitle),
    datasets: phases.map((phase) => ({
      label: phase,
      data: Object.values(mockData.applicationProgressionByJobTitle).map(
        (jobData) => {
          const total = Object.values(jobData).reduce(
            (sum, count) => sum + count,
            0
          );
          const phaseCount = jobData[phase] || 0;
          const percentage = (phaseCount / total) * 100;
          return percentage.toFixed(2);
        }
      ),
      backgroundColor: getPhaseColor(phase),
    })),
  };

  const progressionByJobTitleOptions = {
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
          text: 'Job Title',
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
          <Bar data={progressionByLocationData} options={progressionByLocationOptions} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Progression vs Company</h2>
        <div className="chart-container">
          <Bar data={progressionByCompanyData} options={progressionByCompanyOptions} />
        </div>
      </section>

      <section className="analytics-section">
        <h2>Application Progression vs Job Title</h2>
        <div className="chart-container">
          <Bar data={progressionByJobTitleData} options={progressionByJobTitleOptions} />
        </div>
      </section>
    </div>
  );
}

export default Analytics;
