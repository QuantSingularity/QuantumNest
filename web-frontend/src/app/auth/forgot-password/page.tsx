"use client";

import { useRouter } from "next/navigation";
import type React from "react";
import { useState } from "react";
import { Button } from "@/components/ui/Button";

type Step = "email" | "sent";

export default function ForgotPassword() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("email");
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email) {
      setError("Email address is required");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    setIsLoading(true);
    try {
      // In production this calls the backend reset endpoint
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setStep("sent");
    } catch {
      setError("Failed to send reset email. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Reset your password
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {step === "email"
              ? "Enter your email and we'll send you a reset link."
              : "Check your inbox for next steps."}
          </p>
        </div>

        {step === "email" ? (
          <>
            {error && (
              <div
                className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
                role="alert"
              >
                <span className="block sm:inline">{error}</span>
              </div>
            )}

            <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
              <div>
                <label htmlFor="email" className="sr-only">
                  Email address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div>
                <Button type="submit" className="w-full" isLoading={isLoading}>
                  Send reset link
                </Button>
              </div>
            </form>
          </>
        ) : (
          <div className="mt-8">
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
                <svg
                  className="h-6 w-6 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-green-900 mb-2">
                Reset link sent!
              </h3>
              <p className="text-sm text-green-700">
                If an account exists for{" "}
                <span className="font-medium">{email}</span>, you will receive a
                password reset link shortly.
              </p>
            </div>
          </div>
        )}

        <div className="text-center space-y-2">
          <button
            type="button"
            onClick={() => router.push("/auth/login")}
            className="font-medium text-indigo-600 hover:text-indigo-500 text-sm block w-full"
          >
            ← Back to sign in
          </button>
          {step === "sent" && (
            <button
              type="button"
              onClick={() => {
                setStep("email");
                setError("");
              }}
              className="font-medium text-gray-500 hover:text-gray-700 text-sm block w-full"
            >
              Try a different email
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
