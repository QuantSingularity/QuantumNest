"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/layout/Navbar";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { useAuth } from "@/app/auth/AuthContext";
import { useBlockchain } from "@/lib/blockchain";
import { shortenAddress, formatCurrency } from "@/lib/utils";

interface ProfileStats {
  portfolioValue: number;
  totalAssets: number;
  totalTrades: number;
  memberSince: string;
}

export default function Profile() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuth();
  const { account, isConnected, getBalance, disconnectWallet } =
    useBlockchain();
  const [balance, setBalance] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [displayName, setDisplayName] = useState("");
  const [bio, setBio] = useState("");

  const stats: ProfileStats = {
    portfolioValue: 61446.25,
    totalAssets: 5,
    totalTrades: 48,
    memberSince: "March 2025",
  };

  useEffect(() => {
    if (user) {
      setDisplayName(user.username);
    }
  }, [user]);

  useEffect(() => {
    if (isConnected) {
      getBalance()
        .then(setBalance)
        .catch(() => setBalance(null));
    }
  }, [isConnected, getBalance]);

  const handleSaveProfile = () => {
    // In production, persist to backend
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Your Profile
        </h1>

        {/* Profile Header */}
        <Card className="mb-6">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
              {/* Avatar */}
              <div className="h-24 w-24 rounded-full bg-indigo-600 flex items-center justify-center text-white text-3xl font-bold flex-shrink-0">
                {(user?.username?.[0] ?? "Q").toUpperCase()}
              </div>

              {/* Info */}
              <div className="flex-1 text-center sm:text-left">
                {isEditing ? (
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Display Name
                      </label>
                      <input
                        type="text"
                        value={displayName}
                        onChange={(e) => setDisplayName(e.target.value)}
                        className="w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Bio
                      </label>
                      <textarea
                        value={bio}
                        onChange={(e) => setBio(e.target.value)}
                        rows={3}
                        placeholder="Tell us about yourself..."
                        className="w-full max-w-sm px-3 py-2 border border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                      />
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" onClick={handleSaveProfile}>
                        Save
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setIsEditing(false)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {displayName || user?.username || "QuantumNest User"}
                    </h2>
                    <p className="text-gray-500 dark:text-gray-400 mt-1">
                      {user?.email ?? ""}
                    </p>
                    {bio && (
                      <p className="text-gray-600 dark:text-gray-300 mt-2 max-w-md">
                        {bio}
                      </p>
                    )}
                    <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                      Member since {stats.memberSince}
                    </p>
                    <Button
                      size="sm"
                      variant="outline"
                      className="mt-3"
                      onClick={() => setIsEditing(true)}
                    >
                      Edit Profile
                    </Button>
                  </>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            {
              label: "Portfolio Value",
              value: formatCurrency(stats.portfolioValue),
            },
            { label: "Total Assets", value: stats.totalAssets },
            { label: "Total Trades", value: stats.totalTrades },
            { label: "Member Since", value: stats.memberSince },
          ].map((stat) => (
            <Card key={stat.label}>
              <CardContent className="p-4 text-center">
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {stat.label}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Wallet Section */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Wallet</CardTitle>
          </CardHeader>
          <CardContent>
            {isConnected && account ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-500 dark:text-gray-400">
                    Address
                  </span>
                  <span className="font-mono text-gray-900 dark:text-white">
                    {shortenAddress(account, 8)}
                  </span>
                </div>
                {balance !== null && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500 dark:text-gray-400">
                      ETH Balance
                    </span>
                    <span className="font-medium text-gray-900 dark:text-white">
                      {parseFloat(balance).toFixed(4)} ETH
                    </span>
                  </div>
                )}
                <Button variant="outline" size="sm" onClick={disconnectWallet}>
                  Disconnect Wallet
                </Button>
              </div>
            ) : (
              <div className="text-center py-4">
                <p className="text-gray-500 dark:text-gray-400 mb-3">
                  No wallet connected
                </p>
                <Button size="sm" onClick={() => router.push("/")}>
                  Connect Wallet
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Account Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Account</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button
              variant="outline"
              className="w-full sm:w-auto"
              onClick={() => router.push("/settings")}
            >
              Account Settings
            </Button>
            {isAuthenticated && (
              <Button
                variant="destructive"
                className="w-full sm:w-auto sm:ml-3"
                onClick={logout}
              >
                Sign Out
              </Button>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
