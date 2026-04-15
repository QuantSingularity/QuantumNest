"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        {/* Large 404 */}
        <div className="relative mb-6">
          <p className="text-9xl font-extrabold text-indigo-600 dark:text-indigo-500 select-none opacity-20">
            404
          </p>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="h-16 w-16 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-8 h-8 text-indigo-600 dark:text-indigo-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
                />
              </svg>
            </div>
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
          Page Not Found
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
          Let&apos;s get you back on track.
        </p>

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link href="/">
            <Button>Go Home</Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline">Dashboard</Button>
          </Link>
        </div>

        <div className="mt-10 grid grid-cols-2 gap-3 text-sm">
          {[
            { href: "/portfolio", label: "Portfolio" },
            { href: "/market-analysis", label: "Market Analysis" },
            { href: "/recommendations", label: "Recommendations" },
            { href: "/blockchain-explorer", label: "Blockchain Explorer" },
          ].map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300 font-medium"
            >
              {link.label} →
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
