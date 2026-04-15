"use client";

// FIXED: Table component was called with non-existent `headers` and `data` props
// (the Table component in this codebase only accepts children, not those props).
// Rewrote all table usage to use proper TableHeader/TableBody/TableRow/TableCell sub-components.
// FIXED: Added Navbar component (was missing while all other pages have it).
// FIXED: Typed state properly to avoid implicit 'any' issues.

import { useRouter } from "next/navigation";
import type React from "react";
import { useEffect, useState } from "react";
import Navbar from "@/components/layout/Navbar";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";

interface AdminUser {
  id: string;
  username: string;
  email: string;
  role: string;
  status: string;
}

interface AdminTransaction {
  id: string;
  username: string;
  type: string;
  amount: number;
  status: string;
  timestamp: string;
}

interface SystemStats {
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  activeUsers: number;
  totalTransactions: number;
  apiRequests: number;
}

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
}

interface UserFormData {
  id: string;
  username: string;
  email: string;
  role: string;
  status: string;
}

export default function Admin() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("users");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [transactions, setTransactions] = useState<AdminTransaction[]>([]);
  const [systemStats, setSystemStats] = useState<SystemStats>({
    cpuUsage: 0,
    memoryUsage: 0,
    diskUsage: 0,
    activeUsers: 0,
    totalTransactions: 0,
    apiRequests: 0,
  });
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [userModalOpen, setUserModalOpen] = useState(false);
  const [userFormData, setUserFormData] = useState<UserFormData>({
    id: "",
    username: "",
    email: "",
    role: "user",
    status: "active",
  });

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        setLoading(true);

        const usersResponse = await fetch("/api/admin/users");
        if (!usersResponse.ok) throw new Error("Failed to fetch users");
        const usersData = await usersResponse.json();
        setUsers(usersData);

        const transactionsResponse = await fetch("/api/admin/transactions");
        if (!transactionsResponse.ok)
          throw new Error("Failed to fetch transactions");
        const transactionsData = await transactionsResponse.json();
        setTransactions(transactionsData);

        const statsResponse = await fetch("/api/admin/system-stats");
        if (!statsResponse.ok) throw new Error("Failed to fetch system stats");
        const statsData = await statsResponse.json();
        setSystemStats(statsData);

        const logsResponse = await fetch("/api/admin/logs");
        if (!logsResponse.ok) throw new Error("Failed to fetch logs");
        const logsData = await logsResponse.json();
        setLogs(logsData);

        setLoading(false);
      } catch (err) {
        console.error("Error fetching admin data:", err);
        setError("Failed to load admin data. Please try again later.");
        setLoading(false);
      }
    };

    fetchAdminData();
    const interval = setInterval(fetchAdminData, 60000);
    return () => clearInterval(interval);
  }, []);

  const handleUserEdit = (user: AdminUser) => {
    setSelectedUser(user);
    setUserFormData({
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      status: user.status,
    });
    setUserModalOpen(true);
  };

  const handleUserDelete = async (userId: string) => {
    if (!confirm("Are you sure you want to delete this user?")) return;

    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete user");
      setUsers(users.filter((user) => user.id !== userId));
    } catch (err) {
      console.error("Error deleting user:", err);
      setError("Failed to delete user. Please try again.");
    }
  };

  const handleUserFormChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setUserFormData({ ...userFormData, [name]: value });
  };

  const handleUserFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const method = selectedUser ? "PUT" : "POST";
      const url = selectedUser
        ? `/api/admin/users/${userFormData.id}`
        : "/api/admin/users";

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userFormData),
      });

      if (!response.ok)
        throw new Error(`Failed to ${selectedUser ? "update" : "create"} user`);

      const updatedUser: AdminUser = await response.json();

      if (selectedUser) {
        setUsers(users.map((u) => (u.id === updatedUser.id ? updatedUser : u)));
      } else {
        setUsers([...users, updatedUser]);
      }

      setUserModalOpen(false);
      setSelectedUser(null);
      setUserFormData({
        id: "",
        username: "",
        email: "",
        role: "user",
        status: "active",
      });
    } catch (err) {
      console.error("Error saving user:", err);
      setError(
        `Failed to ${selectedUser ? "update" : "create"} user. Please try again.`,
      );
    }
  };

  // FIXED: Rewrote renderUsersTab to use proper Table sub-components instead of
  // the non-existent `headers` / `data` props pattern.
  const renderUsersTab = () => (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">User Management</h2>
        <Button
          onClick={() => {
            setSelectedUser(null);
            setUserFormData({
              id: "",
              username: "",
              email: "",
              role: "user",
              status: "active",
            });
            setUserModalOpen(true);
          }}
        >
          Add New User
        </Button>
      </div>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Username</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={5}
                  className="text-center text-gray-500 py-8"
                >
                  No users found.
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <span className="capitalize">{user.role}</span>
                  </TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        user.status === "active"
                          ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                          : user.status === "suspended"
                            ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                            : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
                      }`}
                    >
                      {user.status}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex space-x-2">
                      <button
                        className="text-blue-500 hover:text-blue-700 text-sm font-medium"
                        onClick={() => handleUserEdit(user)}
                      >
                        Edit
                      </button>
                      <button
                        className="text-red-500 hover:text-red-700 text-sm font-medium"
                        onClick={() => handleUserDelete(user.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );

  // FIXED: Same fix for renderTransactionsTab.
  const renderTransactionsTab = () => (
    <div>
      <h2 className="text-xl font-semibold mb-4">Transaction History</h2>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>User</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Amount</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={6}
                  className="text-center text-gray-500 py-8"
                >
                  No transactions found.
                </TableCell>
              </TableRow>
            ) : (
              transactions.map((tx) => (
                <TableRow key={tx.id}>
                  <TableCell className="font-mono text-xs">{tx.id}</TableCell>
                  <TableCell>{tx.username}</TableCell>
                  <TableCell>{tx.type}</TableCell>
                  <TableCell>${tx.amount.toFixed(2)}</TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        tx.status === "completed"
                          ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                          : tx.status === "failed"
                            ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                            : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200"
                      }`}
                    >
                      {tx.status}
                    </span>
                  </TableCell>
                  <TableCell>
                    {new Date(tx.timestamp).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );

  const renderSystemTab = () => (
    <div>
      <h2 className="text-xl font-semibold mb-4">System Statistics</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">CPU Usage</h3>
          <div className="text-3xl font-bold">{systemStats.cpuUsage}%</div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-blue-600 h-2.5 rounded-full"
              style={{ width: `${systemStats.cpuUsage}%` }}
            />
          </div>
        </Card>
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">Memory Usage</h3>
          <div className="text-3xl font-bold">{systemStats.memoryUsage}%</div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-green-600 h-2.5 rounded-full"
              style={{ width: `${systemStats.memoryUsage}%` }}
            />
          </div>
        </Card>
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">Disk Usage</h3>
          <div className="text-3xl font-bold">{systemStats.diskUsage}%</div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className="bg-yellow-600 h-2.5 rounded-full"
              style={{ width: `${systemStats.diskUsage}%` }}
            />
          </div>
        </Card>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">Active Users</h3>
          <div className="text-3xl font-bold">{systemStats.activeUsers}</div>
        </Card>
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">Total Transactions</h3>
          <div className="text-3xl font-bold">
            {systemStats.totalTransactions}
          </div>
        </Card>
        <Card className="p-4">
          <h3 className="text-lg font-medium mb-2">API Requests (24h)</h3>
          <div className="text-3xl font-bold">{systemStats.apiRequests}</div>
        </Card>
      </div>
    </div>
  );

  const renderLogsTab = () => (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">System Logs</h2>
        <div className="flex space-x-2">
          <select className="border rounded p-1 text-sm dark:bg-gray-800 dark:border-gray-700">
            <option value="all">All Levels</option>
            <option value="error">Errors</option>
            <option value="warning">Warnings</option>
            <option value="info">Info</option>
            <option value="debug">Debug</option>
          </select>
          <Button size="sm">Download Logs</Button>
        </div>
      </div>
      <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded font-mono text-sm h-96 overflow-y-auto">
        {logs.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No logs available.
          </div>
        ) : (
          logs.map((log, index) => (
            <div
              key={index}
              className={`mb-1 ${
                log.level === "error"
                  ? "text-red-600"
                  : log.level === "warning"
                    ? "text-yellow-600"
                    : log.level === "info"
                      ? "text-blue-600"
                      : "text-gray-600 dark:text-gray-400"
              }`}
            >
              [{new Date(log.timestamp).toLocaleString()}] [
              {log.level.toUpperCase()}] {log.message}
            </div>
          ))
        )}
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case "users":
        return renderUsersTab();
      case "transactions":
        return renderTransactionsTab();
      case "system":
        return renderSystemTab();
      case "logs":
        return renderLogsTab();
      default:
        return renderUsersTab();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <div className="container mx-auto p-6">
          <h1 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
            Admin Dashboard
          </h1>
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mr-3"></div>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Loading admin data...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white">
          Admin Dashboard
        </h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
          {["users", "transactions", "system", "logs"].map((tab) => (
            <button
              key={tab}
              className={`py-2 px-4 font-medium capitalize ${
                activeTab === tab
                  ? "border-b-2 border-indigo-500 text-indigo-600 dark:text-indigo-400"
                  : "text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
              }`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>

        {renderContent()}

        {userModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                {selectedUser ? "Edit User" : "Add New User"}
              </h2>
              <form onSubmit={handleUserFormSubmit}>
                <div className="mb-4">
                  <label
                    className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300"
                    htmlFor="username"
                  >
                    Username
                  </label>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    value={userFormData.username}
                    onChange={handleUserFormChange}
                    required
                  />
                </div>
                <div className="mb-4">
                  <label
                    className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300"
                    htmlFor="email"
                  >
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    value={userFormData.email}
                    onChange={handleUserFormChange}
                    required
                  />
                </div>
                <div className="mb-4">
                  <label
                    className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300"
                    htmlFor="role"
                  >
                    Role
                  </label>
                  <select
                    id="role"
                    name="role"
                    className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    value={userFormData.role}
                    onChange={handleUserFormChange}
                  >
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                    <option value="moderator">Moderator</option>
                  </select>
                </div>
                <div className="mb-6">
                  <label
                    className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300"
                    htmlFor="status"
                  >
                    Status
                  </label>
                  <select
                    id="status"
                    name="status"
                    className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    value={userFormData.status}
                    onChange={handleUserFormChange}
                  >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="suspended">Suspended</option>
                  </select>
                </div>
                <div className="flex justify-end space-x-4">
                  <Button
                    variant="secondary"
                    onClick={() => setUserModalOpen(false)}
                    type="button"
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    {selectedUser ? "Update User" : "Add User"}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
