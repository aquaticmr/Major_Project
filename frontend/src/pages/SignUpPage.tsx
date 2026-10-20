import React from 'react';
import { SignUp } from '@clerk/clerk-react';

export const SignUpPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-6">
          <div className="inline-block p-3 rounded-2xl bg-emerald-500 text-white font-bold text-2xl mb-2">
            FX
          </div>
          <h1 className="text-2xl font-bold text-white">Create your Account</h1>
          <p className="text-sm text-slate-400 mt-1">Join FinoAddWise-X for private, low-hallucination planning</p>
        </div>
        <div className="flex justify-center">
          <SignUp routing="path" path="/sign-up" signInUrl="/sign-in" redirectUrl="/dashboard" />
        </div>
      </div>
    </div>
  );
};
