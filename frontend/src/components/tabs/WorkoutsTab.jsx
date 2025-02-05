import React, { useState } from "react";
import { FireIcon, CalendarDaysIcon, MapPinIcon, FunnelIcon, ArrowsUpDownIcon } from "@heroicons/react/24/solid";

const WorkoutsTab = ({ classData }) => {
  // Local State for Sorting & Filtering
  const [sortField, setSortField] = useState("date"); // Default sorting by date
  const [sortOrder, setSortOrder] = useState("desc"); // Default newest first
  const [selectedClass, setSelectedClass] = useState("All");
  const [dateRange, setDateRange] = useState("all");
  const [selectedStudio, setSelectedStudio] = useState("All");
  const [visibleWorkouts, setVisibleWorkouts] = useState(8); // Show first 8

// Function to load more workouts
const loadMoreWorkouts = () => {
    setVisibleWorkouts((prev) => prev + 7); // Load 7 more
  };
  
  // Function to show all workouts
  const showAllWorkouts = () => {
    setVisibleWorkouts(filteredWorkouts.length); // Show everything
  };

  // Unique class types for filtering
  const classTypes = ["All", ...new Set(classData.workouts.map(workout => workout.class_name))];
  // Unique studios for filtering
  const studios = ["All", ...new Set(classData.workouts.map(workout => workout.studio))];


  // Sorting Function
  const sortWorkouts = (field) => {
    const order = sortField === field && sortOrder === "desc" ? "asc" : "desc";
    setSortField(field);
    setSortOrder(order);
  };

  const filteredWorkouts = classData.workouts
  // Filter by Class Type
  .filter(workout => selectedClass === "All" || workout.class_name === selectedClass)
  
  // Filter by Studio
  .filter(workout => selectedStudio === "All" || workout.studio === selectedStudio)

  // Filter by Date Range
  .filter(workout => {
    const workoutDate = new Date(workout.date);
    const today = new Date();

    if (dateRange === "7") {
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(today.getDate() - 7);
      return workoutDate >= sevenDaysAgo;
    }
    if (dateRange === "30") {
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(today.getDate() - 30);
      return workoutDate >= thirtyDaysAgo;
    }
    if (dateRange === "180") {
      const sixMonthsAgo = new Date();
      sixMonthsAgo.setMonth(today.getMonth() - 6);
      return workoutDate >= sixMonthsAgo;
    }
    return true; // Ensures "All Time" option includes all workouts
  })

  // Sorting Logic
  .sort((a, b) => {
    if (sortField === "date") {
      return sortOrder === "asc"
        ? new Date(a.date) - new Date(b.date)
        : new Date(b.date) - new Date(a.date);
    } else if (["calories_burned", "splat_points"].includes(sortField)) {
      return sortOrder === "asc" ? a[sortField] - b[sortField] : b[sortField] - a[sortField];
    } else if (["studio", "coach", "class_name"].includes(sortField)) {
      return sortOrder === "asc"
        ? (a[sortField] || "").localeCompare(b[sortField] || "", undefined, { sensitivity: "base" })
        : (b[sortField] || "").localeCompare(a[sortField] || "", undefined, { sensitivity: "base" });
    }
    return 0;
  });
      

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="text-center">
        <h2 className="text-2xl font-semibold bg-gradient-to-r from-orange-400 to-red-500 text-transparent bg-clip-text flex items-center justify-center">
          <FireIcon className="w-5 h-5 text-orange-400 mr-2" />
          HRM-Tracked Workouts
        </h2>
        <p className="text-slate-400 text-sm mt-1">View your recent workouts where you wore a heart rate monitor.</p>
        <div className="mt-4 border-b border-slate-700/50 w-48 mx-auto"></div>
      </div>

{/* 🔹 Polished Filter Section */}
<div className="bg-slate-800/50 p-5 rounded-lg shadow-md border border-slate-700/50">
  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
    
    {/* Class Type Filter */}
    <div className="flex flex-col">
      <label className="text-slate-300 text-sm font-medium mb-1 flex items-center">
        <FunnelIcon className="w-5 h-5 text-orange-400 mr-2" />
        Class Type
      </label>
      <select
        className="bg-slate-900 text-slate-300 text-sm p-3 rounded-md border border-slate-700/50 focus:ring-2 focus:ring-orange-400 hover:bg-slate-800 transition-all"
        value={selectedClass}
        onChange={(e) => setSelectedClass(e.target.value)}
      >
        {classTypes.map((className) => (
          <option key={className} value={className}>
            {className}
          </option>
        ))}
      </select>
    </div>

    {/* Date Range Filter */}
    <div className="flex flex-col">
      <label className="text-slate-300 text-sm font-medium mb-1 flex items-center">
        <CalendarDaysIcon className="w-5 h-5 text-orange-400 mr-2" />
        Date Range
      </label>
      <select
        className="bg-slate-900 text-slate-300 text-sm p-3 rounded-md border border-slate-700/50 focus:ring-2 focus:ring-orange-400 hover:bg-slate-800 transition-all"
        value={dateRange}
        onChange={(e) => setDateRange(e.target.value)}
      >
        <option value="all">All Time</option>
        <option value="7">Last 7 Days</option>
        <option value="30">Last 30 Days</option>
        <option value="180">Last 6 Months</option>
      </select>
    </div>

    {/* Studio Filter */}
    <div className="flex flex-col">
      <label className="text-slate-300 text-sm font-medium mb-1 flex items-center">
        <MapPinIcon className="w-5 h-5 text-purple-400 mr-2" />
        Studio
      </label>
      <select
        className="bg-slate-900 text-slate-300 text-sm p-3 rounded-md border border-slate-700/50 focus:ring-2 focus:ring-purple-400 hover:bg-slate-800 transition-all"
        value={selectedStudio}
        onChange={(e) => setSelectedStudio(e.target.value)}
      >
        {studios.map((studio) => (
          <option key={studio} value={studio}>
            {studio}
          </option>
        ))}
      </select>
    </div>
  </div>
</div>



      {/* Workout Summary */}
      <div className="flex justify-center">
        <div className="px-6 py-4 bg-slate-800/40 rounded-xl shadow-md border border-slate-700/50 flex items-center space-x-3">
          <FireIcon className="w-6 h-6 text-orange-400" />
          <p className="text-slate-300 text-sm">
            You have tracked <span className="text-orange-400 font-bold text-lg">{classData.retrievedWorkouts}</span> out of  
            <span className="text-orange-400 font-bold text-lg"> {classData.total}</span> total workouts with a heart rate monitor.
          </p>
        </div>
      </div>

      {/* Workouts Table */}
      <div className="w-full max-w-[1200px] mx-auto overflow-y-auto max-h-[500px]">
  <table className="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg shadow-lg">
    <thead className="bg-slate-900 text-slate-300 text-sm uppercase tracking-wider sticky top-0 z-10">
      <tr>
        {[
          { field: "date", label: "Date", width: "w-[12%]" },
          { field: "class_name", label: "Class Name", width: "w-[18%]" },
          { field: "coach", label: "Coach", width: "w-[14%]" },
          { field: "calories_burned", label: "Calories", width: "w-[14%]" },
          { field: "splat_points", label: "Splats", width: "w-[12%]" },
          { field: "studio", label: "Studio", width: "w-[20%]" },
        ].map(({ field, label, width }) => (
          <th key={field} className={`px-4 py-3 ${width} text-left cursor-pointer`} onClick={() => sortWorkouts(field)}>
            <div className="flex items-center space-x-1">
              <span>{label}</span>
              {sortField === field && <ArrowsUpDownIcon className="w-3 h-3 text-slate-500" />}
            </div>
          </th>
        ))}
      </tr>
    </thead>
    <tbody>
  {filteredWorkouts.slice(0, visibleWorkouts).map((workout, index) => (
    <tr 
      key={workout.id} 
      className={`text-slate-300 border-b border-slate-700 ${
        index % 2 === 0 ? "bg-slate-800/50" : "bg-slate-800/30"
      } hover:bg-slate-800/70 transition-all`}
    >
      <td className="px-4 py-3 w-[12%]">{new Date(workout.date).toLocaleDateString()}</td>
      <td className="px-4 py-3 w-[18%] truncate max-w-[150px] hover:whitespace-normal" title={workout.class_name}>
        {workout.class_name}
      </td>
      <td className="px-4 py-3 w-[14%] truncate max-w-[120px] hover:whitespace-normal" title={workout.coach}>
        {workout.coach}
      </td>
      <td className="px-4 py-3 w-[14%] text-center text-red-400">{workout.calories_burned}</td>
      <td className="px-4 py-3 w-[12%] text-center text-orange-400">{workout.splat_points}</td>
      <td className="px-4 py-3 w-[20%] truncate max-w-[180px] hover:whitespace-normal" title={workout.studio}>
        {workout.studio}
      </td>
    </tr>
  ))}
</tbody>

  </table>
</div>

{/* Show More / Show All Buttons */}
{filteredWorkouts.length > visibleWorkouts && (
  <div className="flex justify-center space-x-4 mt-4">
    <button 
      onClick={loadMoreWorkouts} 
      className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md transition"
    >
      Load More
    </button>
    <button 
      onClick={showAllWorkouts} 
      className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-md transition"
    >
      Show All
    </button>
  </div>
)}
   </div>
  );
};

export default WorkoutsTab;