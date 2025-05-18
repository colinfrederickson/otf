import React, { useState, useEffect, useCallback } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';
import StatCard from './stats/StatCard';
import  WorkoutsTab from './tabs/WorkoutsTab';
import TrendsTab from "./tabs/TrendsTab";

// Tab content components
const OverviewTab = ({ classData, error, status, memberInfo }) => (
  <div className="text-center space-y-8">
    {/* Total Classes Card */}
    <div className="inline-block p-8 rounded-2xl bg-gradient-to-b from-slate-800/50 to-slate-900/50 
                  border border-slate-700/50 shadow-lg backdrop-blur-sm
                  hover:shadow-orange-500/10 transition-all duration-300">
      <div className="bg-gradient-to-r from-red-500 via-orange-400 to-amber-400 text-transparent bg-clip-text">
        <div className="text-7xl font-bold mb-2">
          {classData.total}
        </div>
        <div className="text-lg font-medium uppercase tracking-wider">
          Total Classes
        </div>
      </div>
    </div>

    {/* Detailed Stats Cards */}
    <div className="grid grid-cols-2 gap-4">
      <div className="p-6 rounded-xl bg-gradient-to-b from-slate-800/50 to-slate-900/50 
                    border border-slate-700/50 shadow-lg backdrop-blur-sm
                    hover:shadow-blue-500/20 transition-all duration-300">
        <div className="bg-gradient-to-r from-blue-500 to-indigo-500 text-transparent bg-clip-text">
          <div className="text-4xl font-bold mb-2">
            {classData.inStudio}
          </div>
          <div className="text-sm font-medium uppercase tracking-wider">
            In-Studio Classes
          </div>
        </div>
      </div>
      <div className="p-6 rounded-xl bg-gradient-to-b from-slate-800/50 to-slate-900/50 
                    border border-slate-700/50 shadow-lg backdrop-blur-sm
                    hover:shadow-purple-500/20 transition-all duration-300">
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-transparent bg-clip-text">
          <div className="text-4xl font-bold mb-2">
            {classData.otLive}
          </div>
          <div className="text-sm font-medium uppercase tracking-wider">
            OTLive Classes
          </div>
        </div>
      </div>
    </div>

    {error && status === 'partial_success' && (
      <div className="text-slate-400 text-sm px-4 py-2 bg-slate-800/30 rounded-lg inline-block">
        {error}
      </div>
    )}
  </div>
);

const Dashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [classData, setClassData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');
  const [memberInfo, setMemberInfo] = useState(null);

  const fetchAllData = useCallback(async () => {
    try {
      const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
      
      if (!token) {
        throw new Error('No authentication token found');
      }
  
      setLoading(true);
      setError(null);
  
      const [classResponse, memberResponse] = await Promise.all([
        fetch('http://localhost:8000/api/total-classes', {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch('http://localhost:8000/api/member-detail', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);
  
      if (classResponse.status === 401 || memberResponse.status === 401) {
        localStorage.removeItem('authToken');
        sessionStorage.removeItem('authToken');
        onLogout?.();
        throw new Error('Session expired. Please login again.');
      }
  
      if (!classResponse.ok || !memberResponse.ok) {
        throw new Error('Failed to fetch data');
      }
  
      const [classData, memberData] = await Promise.all([
        classResponse.json(),
        memberResponse.json()
      ]);
  
      console.log("Workout Data:", classData.performance_data.workouts); // Log full workout data
  
      setClassData({
        total: classData.total_classes.total,
        inStudio: classData.total_classes.in_studio,
        otLive: classData.total_classes.ot_live,
        retrievedWorkouts: classData.performance_data.retrieved_workouts,
        workouts: classData.performance_data.workouts // <-- NEW: Store workouts in state
      });
  
      setMemberInfo(memberData.data);
      setStatus(classData.status);
  
      if (classData.status === 'partial_success') {
        setError('Note: Some workout data could not be processed');
      }
    } catch (err) {
      setError(err.message);
      setStatus('error');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  }, [onLogout]);
  
  

  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  const handleRefresh = () => {
    fetchAllData();
  };

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'workouts', label: 'Workouts' },
    { id: 'trends', label: 'Trends' }
  ];

  // Loading and error states are now centralized
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent mb-4"></div>
          <p className="text-slate-400">Loading your data...</p>
        </div>
      </div>
    );
  }

  if (error && status === 'error') {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="text-red-400 text-sm px-6 py-4 bg-red-900/20 rounded-xl inline-block border border-red-700/50">
            <p className="mb-3">{error}</p>
            <button
              onClick={handleRefresh}
              className="text-orange-400 hover:text-orange-300 underline focus:outline-none"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Only render main content when we have all data
  if (!memberInfo || !classData) return null;

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button 
              onClick={handleRefresh}
              className="text-xl font-bold bg-gradient-to-r from-red-500 via-orange-400 to-amber-400 text-transparent bg-clip-text tracking-tight hover:opacity-80 transition-opacity"
            >
              AFTERBURN
            </button>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-gradient-to-br from-orange-500/10 to-amber-500/10 ring-1 ring-orange-500/20">
                  <span className="text-xs font-medium text-orange-400/90">
                    {`${memberInfo.first_name[0]}${memberInfo.last_name[0]}`}
                  </span>
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-medium text-slate-300 leading-tight">
                    {memberInfo.first_name} {memberInfo.last_name}
                  </span>
                  <span className="text-xs text-slate-500 leading-tight">
                    {memberInfo.studio_info.home_studio_name}
                  </span>
                </div>
              </div>
              {/* Action buttons with consistent styling */}
              <div className="flex items-center gap-2">
                <button
                  onClick={handleRefresh}
                  className="px-3 py-1.5 text-sm font-medium text-slate-400 bg-slate-800/50 rounded-lg 
                           hover:bg-slate-700/50 hover:text-slate-300 focus:outline-none
                           transition-all duration-200 border border-slate-700/50 flex items-center"
                  disabled={loading}
                >
                  <ArrowPathIcon className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
                <button
                  onClick={onLogout}
                  className="px-3 py-1.5 text-sm font-medium text-slate-400 bg-slate-800/50 rounded-lg 
                           hover:bg-slate-700/50 hover:text-slate-300 focus:outline-none
                           transition-all duration-200 border border-slate-700/50"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
{/* Member Stats Section */}
<div className="grid grid-cols-3 gap-4 mb-8">
  <StatCard 
    value={classData.total}
    label="Total Classes"
  />
  
  <StatCard 
    value={`${memberInfo.workout_stats.attendance_rate}%`}
    label="Attendance Rate"
    tooltip="Shows how consistently you attend your scheduled workouts. Higher rates mean you're sticking to your fitness commitments."
  />

  <StatCard 
    value={`${memberInfo.workout_stats.hrm_usage_rate}%`}
    label="HRM Usage"
    tooltip="Tracks how often you use your heart rate monitor in class. Using HRM helps optimize your workout intensity and earn splat points."
  />
</div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden border border-slate-700/50">
          {/* Tabs */}
<div className="flex border-b border-slate-700/50">
{tabs.map((tab) => (
    <button
      key={tab.id}
      onClick={() => setActiveTab(tab.id)}
      className={`px-8 py-4 text-sm font-medium relative transition-colors
        ${activeTab === tab.id 
          ? 'text-orange-400 bg-slate-800/50 backdrop-blur-sm' 
          : 'text-slate-500 hover:text-slate-400'}
      `}
      style={{
        outline: 'none',        
        boxShadow: 'none',      
        border: 'none'          
      }}
      onMouseDown={(e) => e.preventDefault()} // Prevents focus on click
    >
      {tab.label}
      {activeTab === tab.id && (
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-red-500 via-orange-500 to-amber-500"></div>
      )}
    </button>
  ))}
</div>

          
<div className="p-6 sm:p-10">
  {activeTab === 'overview' && (
    <OverviewTab 
      classData={classData} 
      error={error} 
      status={status}
      memberInfo={memberInfo}
    />
  )}
  {activeTab === 'workouts' && (
    <WorkoutsTab classData={classData} />
  )}
{activeTab === 'trends' && classData?.workouts?.length > 0 && (
  <TrendsTab workoutData={classData.workouts} />
)}
</div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;