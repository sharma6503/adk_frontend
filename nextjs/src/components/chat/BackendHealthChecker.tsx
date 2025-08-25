"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import React from "react";

// Utility function to get theme immediately from localStorage
function getStoredTheme(): string {
  if (typeof window === 'undefined') return 'system';
  return localStorage.getItem('upskilling-assistant-theme') || 'system';
}

// Utility function to detect system theme immediately
function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Utility function to resolve the actual theme
function resolveTheme(storedTheme: string): 'light' | 'dark' {
  if (storedTheme === 'system') {
    return getSystemTheme();
  }
  return storedTheme as 'light' | 'dark';
}

interface BackendHealthCheckerProps {
  onHealthStatusChange?: (isHealthy: boolean, isChecking: boolean) => void;
  children?: React.ReactNode;
}

/**
 * Backend health monitoring component that displays appropriate states
 * Uses the useBackendHealth hook for monitoring and retry logic
 */
export function BackendHealthChecker({
  onHealthStatusChange,
  children,
}: BackendHealthCheckerProps) {
  const { isBackendReady, isCheckingBackend, checkBackendHealth } =
    useBackendHealth();

  // Notify parent of health status changes
  React.useEffect(() => {
    if (onHealthStatusChange) {
      onHealthStatusChange(isBackendReady, isCheckingBackend);
    }
  }, [isBackendReady, isCheckingBackend, onHealthStatusChange]);

  // Show loading screen while checking backend
  if (isCheckingBackend) {
    return <BackendLoadingScreen />;
  }

  // Show error screen if backend is not ready
  if (!isBackendReady) {
    return <BackendErrorScreen onRetry={checkBackendHealth} />;
  }

  // Render children if backend is ready
  return <>{children}</>;
}

/**
 * Loading screen component shown while backend is starting up
 */
function BackendLoadingScreen() {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  const storedTheme = getStoredTheme();
  const actualTheme = resolveTheme(storedTheme);
  const currentTheme = theme ? resolveTheme(theme) : actualTheme;
  const isDark = currentTheme === 'dark';
  
  useEffect(() => {
    setMounted(true);
  }, []);
  

  if (!mounted) { return null;}
  // Example: boolean flag for dark mode (could come from context, props, or state)

  return (
    <div
      className={`flex-1 flex flex-col items-center justify-center p-4 overflow-hidden relative ${
        isDark ? "bg-gray-900" : "bg-gray-100"
      }`}
    >
      <div
        className={`w-full max-w-2xl z-10 backdrop-blur-md p-8 rounded-2xl shadow-2xl border ${
          isDark
            ? "bg-gray-800/90 border-gray-700"
            : "bg-white/90 border-gray-200"
        }`}
      >
        <div className="text-center space-y-6">
          <h1
            className={`text-4xl font-bold flex items-center justify-center gap-3 ${
              isDark ? "text-gray-100" : "text-gray-800"
            }`}
          >
            ✨ Upskilling Assistant 🚀
          </h1>

          <div className="flex flex-col items-center space-y-4">
            {/* Spinner */}
            <div className="relative">
              <div
                className={`w-16 h-16 border-4 border-t-blue-500 rounded-full animate-spin ${
                  isDark ? "border-blue-900" : "border-blue-200"
                }`}
              ></div>
              <div
                className="absolute inset-0 w-16 h-16 border-4 border-transparent border-r-purple-500 rounded-full animate-spin"
                style={{
                  animationDirection: "reverse",
                  animationDuration: "1.5s",
                }}
              ></div>
            </div>

            {/* Loading text */}
            <div className="space-y-2">
              <p
                className={`text-xl ${
                  isDark ? "text-gray-200" : "text-gray-700"
                }`}
              >
                Waiting for backend to be ready...
              </p>
              <p
                className={`text-sm ${
                  isDark ? "text-gray-400" : "text-gray-500"
                }`}
              >
                This may take a moment on first startup
              </p>
            </div>

            {/* Animated dots */}
            <div className="flex space-x-1">
              <div
                className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                style={{ animationDelay: "0ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"
                style={{ animationDelay: "150ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-pink-500 rounded-full animate-bounce"
                style={{ animationDelay: "300ms" }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );


  
  // Now we can safely use theme since component is mounted

  
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-4 overflow-hidden relative">
      {/* Background gradient - theme aware */}
      <div className={`absolute inset-0 bg-gradient-to-br ${
        isDark 
          ? 'from-slate-900 via-slate-800 to-slate-900' 
          : 'from-blue-50 via-indigo-50 to-purple-50'
      }`}></div>
      
      <div className={`w-full max-w-2xl z-10 backdrop-blur-md p-8 rounded-2xl shadow-2xl ${
        isDark 
          ? 'bg-slate-800/90 border-slate-700 shadow-black/60' 
          : 'bg-white/90 border-blue-200 shadow-blue-500/20'
      } border`}>
        <div className="text-center space-y-6">
          <h1 className={`text-4xl font-bold flex items-center justify-center gap-3 ${
            isDark ? 'text-white' : 'text-gray-800'
          }`}>
            ✨ Upskilling Assistant 🚀
          </h1>

          <div className="flex flex-col items-center space-y-4">
            {/* Spinning animation */}
            <div className="relative">
              <div className={`w-16 h-16 border-4 border-t-blue-500 rounded-full animate-spin ${
                isDark ? 'border-neutral-600' : 'border-blue-200'
              }`}></div>
              <div
                className="absolute inset-0 w-16 h-16 border-4 border-transparent border-r-purple-500 rounded-full animate-spin"
                style={{
                  animationDirection: "reverse",
                  animationDuration: "1.5s",
                }}
              ></div>
            </div>

            <div className="space-y-2">
              <p className={`text-xl ${
                isDark ? 'text-neutral-300' : 'text-gray-700'
              }`}>
                Waiting for backend to be ready...
              </p>
              <p className={`text-sm ${
                isDark ? 'text-neutral-400' : 'text-gray-500'
              }`}>
                This may take a moment on first startup
              </p>
            </div>

            {/* Animated dots */}
            <div className="flex space-x-1">
              <div
                className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                style={{ animationDelay: "0ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"
                style={{ animationDelay: "150ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-pink-500 rounded-full animate-bounce"
                style={{ animationDelay: "300ms" }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * Error screen component shown when backend is unavailable
 */
function BackendErrorScreen({ onRetry }: { onRetry: () => Promise<boolean> }) {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const handleRetry = () => {
    onRetry().catch((error) => {
      console.error("Retry failed:", error);
    });
  };
  
  // Prevent hydration mismatch by not rendering theme-specific content until mounted
  if (!mounted) {
    // Render with neutral/loading state to prevent hydration mismatch
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-4 relative bg-gray-100">
        <div className="w-full max-w-md z-10 backdrop-blur-md p-6 rounded-2xl shadow-xl bg-white/90 border border-red-200">
          <div className="text-center space-y-4">
            <div className="text-red-500 text-5xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-red-600">Backend Unavailable</h2>
            <p className="text-gray-600">Unable to connect to backend services</p>
            <button
              onClick={handleRetry}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              🔄 Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  // Now we can safely use theme since component is mounted
  const storedTheme = getStoredTheme();
  const actualTheme = resolveTheme(storedTheme);
  const currentTheme = theme ? resolveTheme(theme) : actualTheme;
  const isDark = currentTheme === 'dark';

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-4 relative">
      {/* Background gradient for error state - theme aware */}
      <div className={`absolute inset-0 bg-gradient-to-br ${
        isDark 
          ? 'from-slate-900 via-red-900/20 to-slate-900' 
          : 'from-red-50 via-orange-50 to-yellow-50'
      }`}></div>
      
      <div className={`w-full max-w-md z-10 backdrop-blur-md p-6 rounded-2xl shadow-xl ${
        isDark 
          ? 'bg-slate-800/90 border-red-800 shadow-black/60' 
          : 'bg-white/90 border-red-200 shadow-red-500/20'
      } border`}>
        <div className="text-center space-y-4">
          <div className="text-red-500 text-5xl mb-4">⚠️</div>
          <h2 className={`text-2xl font-bold ${
            isDark ? 'text-red-400' : 'text-red-600'
          }`}>Backend Unavailable</h2>
          <p className={`${
            isDark ? 'text-neutral-300' : 'text-gray-600'
          }`}>
            Unable to connect to backend services
          </p>
          <button
            onClick={handleRetry}
            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            🔄 Try Again
          </button>
        </div>
      </div>
    </div>
  );
}
