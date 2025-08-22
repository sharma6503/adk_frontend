"use client";

import { Pencil, User, Target, Puzzle } from "lucide-react";

export function EmptyState(): React.JSX.Element {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 text-center min-h-[60vh]">
      <div className="max-w-5xl w-full space-y-10">
        {/* Greeting */}
        <div className="space-y-4">
          <h1 className="text-4xl font-bold text-white">👋 Hello! I’m your Upskilling Assistant</h1>
          <p className="text-lg text-neutral-300">
            Here to guide you on your learning journey. Let’s get started — here are the things I can help you with:
          </p>
        </div>

        {/* Feature cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-800/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition">
            <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Pencil className="w-6 h-6 text-green-500" />
            </div>
            <h3 className="font-semibold text-green-400">Update Profile</h3>
            <p className="text-sm text-neutral-400">
              Add or edit your skills, role, and career goals
            </p>
          </div>

          <div className="bg-slate-800/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition">
            <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <User className="w-6 h-6 text-blue-500" />
            </div>
            <h3 className="font-semibold text-blue-400">Show Profile</h3>
            <p className="text-sm text-neutral-400">
              View your current profile details
            </p>
          </div>

          <div className="bg-slate-800/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition">
            <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Target className="w-6 h-6 text-purple-500" />
            </div>
            <h3 className="font-semibold text-purple-400">Get Course Recommendations</h3>
            <p className="text-sm text-neutral-400">
              Personalized learning suggestions just for you
            </p>
          </div>

          <div className="bg-slate-800/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition">
            <div className="w-12 h-12 bg-yellow-500/10 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Puzzle className="w-6 h-6 text-yellow-500" />
            </div>
            <h3 className="font-semibold text-yellow-400">Take a Skill Test</h3>
            <p className="text-sm text-neutral-400">
              Assess your skills and track progress
            </p>
          </div>
        </div>

        {/* Example prompts */}
        <div className="space-y-4">
          <p className="text-neutral-400">Try asking about:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              Recommended courses for AI
            </span>
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              How to improve programming skills
            </span>
            <span className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-sm">
              Career roadmap for Data Science
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
