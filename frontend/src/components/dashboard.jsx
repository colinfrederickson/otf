import React, { useState, useEffect, useCallback } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

// Tab content components
const OverviewTab = ({ classData, error, status }) => (
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



const WorkoutsTab = ({ classData }) => (
  <div className="space-y-6">
    <div className="text-slate-300 text-sm px-4 py-3 bg-slate-800/50 rounded-lg">
      Showing {classData.retrievedWorkouts} recent workouts out of {classData.total} total classes
    </div>
    {/* Placeholder for workout list - to be implemented */}
    <div className="text-center text-slate-400">
      Workout history coming soon...
    </div>
  </div>
);

const Dashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [classData, setClassData] = useState({
    total: 0,
    inStudio: 0,
    otLive: 0,
    retrievedWorkouts: 0
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');

  const fetchData = useCallback(async () => {
    try {
      const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
      
      if (!token) {
        throw new Error('No authentication token found');
      }

      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:8000/api/total-classes', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem('authToken');
          sessionStorage.removeItem('authToken');
          onLogout?.();
          throw new Error('Session expired. Please login again.');
        }
        throw new Error(data.detail || 'Failed to fetch data');
      }

      setClassData({
        total: data.total_classes.total,
        inStudio: data.total_classes.in_studio,
        otLive: data.total_classes.ot_live,
        retrievedWorkouts: data.performance_data.retrieved_workouts
      });
      setStatus(data.status);

      if (data.status === 'partial_success') {
        setError('Note: Some workout data could not be processed');
      }
    } catch (err) {
      setError(err.message);
      setStatus('error');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  }, [onLogout]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'workouts', label: 'Workouts' }
  ];

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button 
              onClick={fetchData}
              className="text-xl font-bold bg-gradient-to-r from-red-500 via-orange-400 to-amber-400 text-transparent bg-clip-text tracking-tight hover:opacity-80 transition-opacity"
            >
              AFTERBURN
            </button>
            <div className="flex items-center space-x-4">
              <button
                onClick={fetchData}
                className="p-2 text-slate-400 hover:text-white focus:outline-none transition-colors"
                disabled={loading}
              >
                <ArrowPathIcon className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
              </button>
              <button
                onClick={onLogout}
                className="px-4 py-2 text-sm font-medium text-slate-300 bg-slate-800/50 rounded-lg 
                         hover:bg-slate-700/50 hover:text-white focus:outline-none focus:ring-2 
                         focus:ring-orange-500/50 focus:ring-offset-2 focus:ring-offset-slate-800 
                         transition-all duration-200 border border-slate-700/50"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden border border-slate-700/50">
        
{/* Tabs */}
<div className="flex border-b border-slate-700/50">
  {tabs.map((tab) => (
    <button
      key={tab.id}
      onClick={() => setActiveTab(tab.id)}
      className={`px-8 py-4 text-sm font-medium relative focus:outline-none transition-colors
                ${activeTab === tab.id 
                  ? 'text-orange-400 bg-slate-800/50 backdrop-blur-sm' 
                  : 'text-slate-500 hover:text-slate-400'}`}
    >
      {tab.label}
      {activeTab === tab.id && (
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-red-500 via-orange-500 to-amber-500"></div>
      )}
    </button>
  ))}
</div>
          
          <div className="p-6 sm:p-10">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-40">
                <div className="animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent mb-4"></div>
                <p className="text-slate-400">Loading your data...</p>
              </div>
            ) : error && status === 'error' ? (
              <div className="text-center space-y-4">
                <div className="text-red-400 text-sm px-6 py-4 bg-red-900/20 rounded-xl inline-block border border-red-700/50">
                  <p className="mb-3">{error}</p>
                  <button
                    onClick={fetchData}
                    className="text-orange-400 hover:text-orange-300 underline focus:outline-none"
                  >
                    Try again
                  </button>
                </div>
              </div>
            ) : (
              activeTab === 'overview' ? (
                <OverviewTab classData={classData} error={error} status={status} />
              ) : (
                <WorkoutsTab classData={classData} />
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;