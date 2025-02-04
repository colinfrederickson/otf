import React from 'react';
import { QuestionMarkCircleIcon } from '@heroicons/react/24/outline';
import { Tooltip } from '../ui/Tooltip';

const StatCard = ({ value, label, tooltip }) => (
  <div className="p-6 rounded-xl bg-gradient-to-b from-slate-800/50 to-slate-900/50 
                  border border-slate-700/50 shadow-lg backdrop-blur-sm
                  hover:shadow-orange-500/10 transition-all duration-300">
    <div className="bg-gradient-to-r from-red-500 via-orange-400 to-amber-400 text-transparent bg-clip-text">
      <div className="flex items-center justify-between mb-2">
        <div className="text-4xl font-bold">{value}</div>
        {tooltip && (
          <Tooltip content={tooltip}>
            <QuestionMarkCircleIcon className="h-5 w-5 text-slate-400 hover:text-slate-300 cursor-help" />
          </Tooltip>
        )}
      </div>
      <div className="text-sm font-medium uppercase tracking-wider">
        {label}
      </div>
    </div>
  </div>
);

export default StatCard;