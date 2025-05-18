import React, { useState, useMemo } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const TrendsChart = ({ workoutData }) => {
  if (!workoutData || workoutData.length === 0) return <p className="text-slate-400 text-center">No workout data available.</p>;

  // 🛠️ State for Toggle (Daily, Weekly, Monthly)
  const [timeFrame, setTimeFrame] = useState("daily");

  // 📊 Aggregated Data Processing (useMemo for performance)
  const processedData = useMemo(() => {
    const aggregateData = (interval) => {
      const grouped = {};
      
      workoutData.forEach((workout) => {
        const date = new Date(workout.date);
        let key = date.toLocaleDateString(); // Default to daily

        if (interval === "weekly") {
          // Get first day of the week (Sunday-based)
          const weekStart = new Date(date.setDate(date.getDate() - date.getDay()));
          key = weekStart.toLocaleDateString();
        } else if (interval === "monthly") {
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`; // YYYY-MM format
        }

        if (!grouped[key]) {
          grouped[key] = { totalCalories: 0, totalSplats: 0, count: 0 };
        }

        grouped[key].totalCalories += workout.calories_burned;
        grouped[key].totalSplats += workout.splat_points;
        grouped[key].count += 1;
      });

      return Object.entries(grouped).map(([key, value]) => ({
        date: key,
        avgCalories: (value.totalCalories / value.count).toFixed(1),
        avgSplats: (value.totalSplats / value.count).toFixed(1),
      }));
    };

    return aggregateData(timeFrame);
  }, [workoutData, timeFrame]);

  // 🎨 Chart Data Preparation
  const labels = processedData.map((d) => d.date);
  const caloriesData = processedData.map((d) => d.avgCalories);
  const splatsData = processedData.map((d) => d.avgSplats);

  const data = {
    labels,
    datasets: [
      {
        label: "Calories Burned",
        data: caloriesData,
        borderColor: "#ff7f50", // Coral color
        backgroundColor: "rgba(255,127,80,0.2)",
        tension: 0.3,
        fill: true,
        yAxisID: "y1"
      },
      {
        label: "Splat Points",
        data: splatsData,
        borderColor: "#ffa500", // Orange
        backgroundColor: "rgba(255,165,0,0.2)",
        tension: 0.3,
        fill: true,
        yAxisID: "y2"
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: { color: "#e2e8f0" }
      },
      tooltip: {
        mode: "index",
        intersect: false
      }
    },
    scales: {
      x: {
        ticks: { color: "#cbd5e1" },
        grid: { color: "#334155" }
      },
      y1: {
        type: "linear",
        position: "left",
        ticks: { color: "#ff7f50" }, // Calories Scale (Coral)
        grid: { color: "#334155" }
      },
      y2: {
        type: "linear",
        position: "right",
        ticks: { color: "#ffa500" }, // Splats Scale (Orange)
        grid: { drawOnChartArea: false }
      }
    }
  };

  return (
    <div className="p-6 bg-slate-800/50 rounded-lg shadow-md border border-slate-700/50">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-semibold text-orange-400">Workout Trends Over Time</h3>
        {/* 📌 Dropdown Toggle */}
        <select
          className="bg-slate-900 text-slate-300 text-sm px-3 py-1 rounded-md border border-slate-700/50 focus:ring-2 focus:ring-orange-400"
          value={timeFrame}
          onChange={(e) => setTimeFrame(e.target.value)}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly Avg</option>
          <option value="monthly">Monthly Avg</option>
        </select>
      </div>
      <Line data={data} options={options} />
    </div>
  );
};

export default TrendsChart;
