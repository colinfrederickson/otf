import React, { useMemo } from "react";
import { FireIcon, ChartBarIcon, SparklesIcon, TrophyIcon, BoltIcon } from "@heroicons/react/24/solid";
import TrendsChart from "../charts/TrendsChart"; // 📊 Import the chart component
import { Tooltip } from "../ui/Tooltip"; // 🛠️ Ensure correct import
import { QuestionMarkCircleIcon } from '@heroicons/react/24/outline';

/**
 * 📌 **TrendsTab Component**
 * - Analyzes and displays **workout trends** over time.
 * - Shows **total workouts, averages, best performing days**, and **personal records (PRs)**.
 */
const TrendsTab = ({ workoutData }) => {
  // ✅ Ensure data is available before processing
  const hasData = workoutData && workoutData.length > 0;

  /**
   * 🧠 **Compute Workout Trends Efficiently**
   * - Uses `useMemo` to **optimize performance** by memoizing calculations.
   */
  const trends = useMemo(() => {
    if (!hasData) return null;

    // 🔢 Aggregate Workout Stats
    const totalWorkouts = workoutData.length;
    const totalCalories = workoutData.reduce((sum, w) => sum + (w.calories_burned || 0), 0);
    const totalSplats = workoutData.reduce((sum, w) => sum + (w.splat_points || 0), 0);
    const avgCalories = totalWorkouts > 0 ? (totalCalories / totalWorkouts).toFixed(1) : 0;
    const avgSplats = totalWorkouts > 0 ? (totalSplats / totalWorkouts).toFixed(1) : 0;

    // 📅 **Best Performing Day Calculation** (Based on Avg Calories Burned)
    const dayPerformance = workoutData.reduce((acc, workout) => {
      const day = new Date(workout.date).toLocaleDateString("en-US", { weekday: "long" });

      if (!acc[day]) {
        acc[day] = { totalCalories: 0, count: 0 };
      }

      acc[day].totalCalories += workout.calories_burned || 0;
      acc[day].count += 1;
      return acc;
    }, {});

    // 🏆 Determine the best-performing day
    const bestDay = Object.keys(dayPerformance).reduce((best, current) => {
      const bestAvg = dayPerformance[best]?.count > 0 ? dayPerformance[best].totalCalories / dayPerformance[best].count : 0;
      const currentAvg = dayPerformance[current]?.count > 0 ? dayPerformance[current].totalCalories / dayPerformance[current].count : 0;
      return currentAvg > bestAvg ? current : best;
    }, "Unknown"); // ✅ Default to "Unknown" if no valid data

    // 🏅 **Personal Records (PRs)**
    const highestCalories = Math.max(...workoutData.map(w => w.calories_burned || 0));
    const highestSplats = Math.max(...workoutData.map(w => w.splat_points || 0));

    // 🔥 **Class Type Performance Breakdown**
    const classPerformance = workoutData.reduce((acc, workout) => {
      if (!acc[workout.class_name]) {
        acc[workout.class_name] = { totalCalories: 0, totalSplats: 0, count: 0 };
      }

      acc[workout.class_name].totalCalories += workout.calories_burned || 0;
      acc[workout.class_name].totalSplats += workout.splat_points || 0;
      acc[workout.class_name].count += 1;
      return acc;
    }, {});

    // 🔥 **Streak Tracking**
    let currentStreak = 0, longestStreak = 0, hrmStreak = 0;
    let lastWorkoutDate = null, tempStreak = 0, tempHRMStreak = 0;

    workoutData
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .forEach((workout) => {
        const workoutDate = new Date(workout.date).setHours(0, 0, 0, 0);
        
        if (lastWorkoutDate) {
          const diff = (workoutDate - lastWorkoutDate) / (1000 * 60 * 60 * 24);
          
          if (diff === 1) {
            tempStreak++;
          } else {
            longestStreak = Math.max(longestStreak, tempStreak);
            tempStreak = 1;
          }

          if (workout.calories_burned > 0) {
            tempHRMStreak++;
          } else {
            hrmStreak = Math.max(hrmStreak, tempHRMStreak);
            tempHRMStreak = 0;
          }
        } else {
          tempStreak = 1;
          tempHRMStreak = workout.calories_burned > 0 ? 1 : 0;
        }

        lastWorkoutDate = workoutDate;
      });

    longestStreak = Math.max(longestStreak, tempStreak);
    hrmStreak = Math.max(hrmStreak, tempHRMStreak);
    currentStreak = tempStreak;

    return {
      totalWorkouts,
      avgCalories,
      avgSplats,
      bestDay,
      highestCalories,
      highestSplats,
      classPerformance,
      currentStreak,
      longestStreak,
      hrmStreak
    };
  }, [workoutData]);

  return (
    <div className="space-y-6">
      {/* 🏆 Header */}
      <div className="text-center">
        <h2 className="text-2xl font-semibold bg-gradient-to-r from-orange-400 to-red-500 text-transparent bg-clip-text flex items-center justify-center">
          <ChartBarIcon className="w-5 h-5 text-orange-400 mr-2" />
          Workout Trends & Insights
        </h2>
        <p className="text-slate-400 text-sm mt-1">Analyze your workout history and trends over time.</p>
      </div>

            {/* 🏅 Streaks */}
            <div className="grid grid-cols-3 gap-4">
        <StatCard icon={<BoltIcon className="w-6 h-6 text-teal-400 mx-auto" />} value={trends?.currentStreak || 0} label="Current Streak (Days)" />
        <StatCard icon={<TrophyIcon className="w-6 h-6 text-yellow-400 mx-auto" />} value={trends?.longestStreak || 0} label="Longest Streak" />
        <StatCard icon={<FireIcon className="w-6 h-6 text-orange-400 mx-auto" />} value={trends?.hrmStreak || 0} label="HRM Streak" />
      </div>

      {/* 📊 Summary Statistics */}
      <div className="grid grid-cols-3 gap-4">
        <StatCard icon={<FireIcon className="w-6 h-6 text-red-400 mx-auto" />} value={trends?.totalWorkouts || 0} label="Total Workouts" />
        <StatCard icon={<FireIcon className="w-6 h-6 text-orange-400 mx-auto" />} value={trends?.avgCalories || 0} label="Avg Calories Burned" />
        <StatCard icon={<FireIcon className="w-6 h-6 text-yellow-400 mx-auto" />} value={trends?.avgSplats || 0} label="Avg Splats" />
      </div>

      {/* 📅 Best Performing Day */}
      <div className="p-6 rounded-xl bg-slate-800/50 border border-slate-700/50 shadow-lg flex items-center space-x-4">
        <SparklesIcon className="w-8 h-8 text-indigo-400" />
        <div>
          <p className="text-lg font-semibold text-slate-300 flex items-center">
            Best Performing Day:
            <Tooltip content="This is determined by the day of the week with the highest average calories burned across all your workouts.">
              <QuestionMarkCircleIcon className="w-4 h-4 ml-2 text-slate-400 hover:text-slate-300 cursor-help transition-colors duration-200" />
            </Tooltip>
          </p>
          <p className="text-xl text-indigo-400 font-bold">{trends?.bestDay || "Unknown"}</p>
        </div>
      </div>

      {/* 🏆 Personal Records */}
      <div className="grid grid-cols-2 gap-4">
        <StatCard icon={<TrophyIcon className="w-6 h-6 text-yellow-400 mx-auto" />} value={trends?.highestCalories} label="Most Calories Burned" />
        <StatCard icon={<TrophyIcon className="w-6 h-6 text-orange-400 mx-auto" />} value={trends?.highestSplats} label="Most Splats Earned" />
      </div>

      {/* 📈 Workout Trends Chart */}
      <TrendsChart workoutData={workoutData} />

      <div className="p-6 bg-slate-800/50 rounded-lg shadow-md border border-slate-700/50">
  <h3 className="text-lg font-semibold text-orange-400 mb-3">Performance by Class Type</h3>

  {trends?.classPerformance && Object.keys(trends.classPerformance).length > 0 ? (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-slate-800/50 border border-slate-700/50 rounded-lg shadow-lg">
        <thead className="bg-slate-900 text-slate-300 text-sm uppercase tracking-wider">
          <tr>
            <th className="px-4 py-3 text-left">Class Type</th>
            <th className="px-4 py-3 text-center">Avg Calories Burned</th>
            <th className="px-4 py-3 text-center">Avg Splats</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(trends.classPerformance).map(([className, stats], index) => (
            <tr key={className} className={`text-slate-300 border-b border-slate-700 ${
              index % 2 === 0 ? "bg-slate-800/50" : "bg-slate-800/30"
            } hover:bg-slate-800/70 transition-all`}>
              <td className="px-4 py-3">{className}</td>
              <td className="px-4 py-3 text-center text-red-400">
                {(stats.totalCalories / stats.count).toFixed(1)} kcal
              </td>
              <td className="px-4 py-3 text-center text-orange-400">
                {(stats.totalSplats / stats.count).toFixed(1)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <p className="text-slate-400 text-sm text-center">No class type data available.</p>
  )}
      </div>
    </div>
  );
};

/** 📌 **Reusable StatCard Component** */
const StatCard = ({ icon, value, label }) => (
  <div className="p-6 rounded-xl bg-slate-800/50 border border-slate-700/50 shadow-lg text-center">
    {icon}
    <p className="text-4xl font-bold text-slate-300">{value}</p>
    <p className="text-sm text-slate-400">{label}</p>
  </div>
);

export default TrendsTab;