import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/solid';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { loginUser } from '../utils/api';

const Login = ({ onLoginSuccess }) => {
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const schema = yup.object().shape({
    email: yup.string().email('Please enter a valid email').required('Email is required'),
    password: yup.string().required('Password is required'),
  });

  const { register, handleSubmit, formState: { errors } } = useForm({ resolver: yupResolver(schema) });

  const onSubmit = async (data) => {
    setError('');
    setLoading(true);

    try {
      const token = await loginUser(data, rememberMe);
      onLoginSuccess(token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center font-sans">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-red-500 via-orange-400 to-amber-400 text-transparent bg-clip-text tracking-tight">
            AFTERBURN
          </h1>
        </div>
        
        <div className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-2xl shadow-2xl border border-slate-700/50">
          <div className="text-center mb-6">
            <h2 className="text-xl font-semibold text-slate-200 mt-2">
              Welcome to Afterburn 🔥
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Sign in with your OTF credentials to begin
            </p>
          </div>
          
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {/* Email Input */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-1">
                Email address
              </label>
              <input
                id="email"
                type="email"
                {...register('email')}
                className={`block w-full px-4 py-3 bg-slate-900/50 border border-slate-700/50 rounded-lg shadow-sm 
                          focus:ring-orange-500/50 focus:border-orange-500/50 
                          placeholder-slate-500 text-slate-200 backdrop-blur-sm focus:outline-none 
                          ${errors.email ? 'border-red-500/50' : ''}`}
                placeholder="Enter your email"
              />
              {errors.email && <p className="text-red-400 text-xs mt-1">{errors.email.message}</p>}
            </div>

            {/* Password Input with Toggle Visibility */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'} // FIXED: Now shows text when visible
                  {...register('password')}
                  className={`block w-full px-4 py-3 bg-slate-900/50 border border-slate-700/50 rounded-lg shadow-sm 
                            focus:ring-orange-500/50 focus:border-orange-500/50 
                            placeholder-slate-500 text-slate-200 backdrop-blur-sm focus:outline-none pr-10 
                            ${errors.password ? 'border-red-500/50' : ''}`}
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-3 flex items-center text-slate-400 hover:text-slate-300 focus:outline-none transition-all"
                  style={{ background: 'none', padding: '0', border: 'none' }} // FIXED: Removed unwanted outline & background
                >
                  {showPassword ? <EyeIcon className="h-5 w-5" /> : <EyeSlashIcon className="h-5 w-5" />}
                </button>
              </div>
              {errors.password && <p className="text-red-400 text-xs mt-1">{errors.password.message}</p>}
            </div>

            {/* Remember Me Checkbox */}
            <div className="flex items-center">
              <input
                id="remember-me"
                type="checkbox"
                className="h-4 w-4 border-2 border-slate-700 rounded focus:ring-orange-500/50 bg-slate-800 transition-all"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-slate-300">
                Remember me
              </label>
            </div>
            
            {/* Error Message */}
            {error && <div className="text-red-400 text-sm mt-2">{error}</div>}
            
            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={loading}
                className={`w-full py-3 px-4 bg-gradient-to-r from-red-500 via-orange-500 to-amber-500 
                          text-white rounded-lg font-medium focus:outline-none focus:ring-2 
                          focus:ring-orange-500/50 focus:ring-offset-2 focus:ring-offset-slate-800 
                          shadow-lg hover:shadow-orange-500/25 transform hover:-translate-y-0.5 transition-all duration-200
                          ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Signing in...
                  </div>
                ) : (
                  'Sign in'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
