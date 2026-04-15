"use client";

// FIXED: Updated to Headless UI v2 API - sub-components like Menu.Button, Menu.Items,
// Disclosure.Button etc. were removed in v2. Now uses exported MenuButton, MenuItems,
// MenuItem, DisclosureButton, DisclosurePanel.
// FIXED: Now uses BlockchainContext for actual wallet state instead of local dummy state.

import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from "@headlessui/react";
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/app/auth/AuthContext";
import { useBlockchain } from "@/lib/blockchain";
import { shortenAddress } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/dashboard" },
  { name: "Portfolio", href: "/portfolio" },
  { name: "Market Analysis", href: "/market-analysis" },
  { name: "Recommendations", href: "/recommendations" },
  { name: "Blockchain Explorer", href: "/blockchain-explorer" },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function Navbar() {
  const pathname = usePathname();
  const { account, isConnected, connectWallet, disconnectWallet } =
    useBlockchain();
  const { logout, isAuthenticated } = useAuth();

  return (
    <Disclosure as="nav" className="bg-gray-900">
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 justify-between">
              <div className="flex">
                <div className="flex flex-shrink-0 items-center">
                  <Link href="/" className="flex items-center">
                    <span className="text-white font-bold text-xl">
                      QuantumNest
                    </span>
                  </Link>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={classNames(
                        pathname === item.href
                          ? "border-indigo-500 text-white"
                          : "border-transparent text-gray-300 hover:border-gray-300 hover:text-white",
                        "inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium",
                      )}
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>

              <div className="hidden sm:ml-6 sm:flex sm:items-center">
                {!isConnected ? (
                  <button
                    onClick={connectWallet}
                    className="rounded-md bg-indigo-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    Connect Wallet
                  </button>
                ) : (
                  <div className="flex items-center space-x-4">
                    <span className="text-gray-300 text-sm">
                      {account ? shortenAddress(account) : ""}
                    </span>
                    <button
                      type="button"
                      className="rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                    >
                      <span className="sr-only">View notifications</span>
                      <BellIcon className="h-6 w-6" aria-hidden="true" />
                    </button>

                    {/* Profile dropdown */}
                    <Menu as="div" className="relative ml-3">
                      <div>
                        <MenuButton className="flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                          <span className="sr-only">Open user menu</span>
                          <div className="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                            QN
                          </div>
                        </MenuButton>
                      </div>
                      <MenuItems
                        transition
                        className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none transition data-[closed]:scale-95 data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75"
                      >
                        <MenuItem>
                          {({ focus }) => (
                            <Link
                              href="/profile"
                              className={classNames(
                                focus ? "bg-gray-100" : "",
                                "block px-4 py-2 text-sm text-gray-700",
                              )}
                            >
                              Your Profile
                            </Link>
                          )}
                        </MenuItem>
                        <MenuItem>
                          {({ focus }) => (
                            <Link
                              href="/settings"
                              className={classNames(
                                focus ? "bg-gray-100" : "",
                                "block px-4 py-2 text-sm text-gray-700",
                              )}
                            >
                              Settings
                            </Link>
                          )}
                        </MenuItem>
                        {isAuthenticated && (
                          <MenuItem>
                            {({ focus }) => (
                              <button
                                onClick={logout}
                                className={classNames(
                                  focus ? "bg-gray-100" : "",
                                  "block w-full text-left px-4 py-2 text-sm text-gray-700",
                                )}
                              >
                                Sign out
                              </button>
                            )}
                          </MenuItem>
                        )}
                        <MenuItem>
                          {({ focus }) => (
                            <button
                              onClick={disconnectWallet}
                              className={classNames(
                                focus ? "bg-gray-100" : "",
                                "block w-full text-left px-4 py-2 text-sm text-gray-700",
                              )}
                            >
                              Disconnect Wallet
                            </button>
                          )}
                        </MenuItem>
                      </MenuItems>
                    </Menu>
                  </div>
                )}
              </div>

              <div className="-mr-2 flex items-center sm:hidden">
                <DisclosureButton className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </DisclosureButton>
              </div>
            </div>
          </div>

          <DisclosurePanel className="sm:hidden">
            <div className="space-y-1 px-2 pb-3 pt-2">
              {navigation.map((item) => (
                <DisclosureButton
                  key={item.name}
                  as="a"
                  href={item.href}
                  className={classNames(
                    pathname === item.href
                      ? "bg-gray-800 text-white"
                      : "text-gray-300 hover:bg-gray-700 hover:text-white",
                    "block rounded-md px-3 py-2 text-base font-medium",
                  )}
                >
                  {item.name}
                </DisclosureButton>
              ))}
              {!isConnected && (
                <button
                  onClick={connectWallet}
                  className="mt-4 w-full rounded-md bg-indigo-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
                >
                  Connect Wallet
                </button>
              )}
            </div>
            {isConnected && (
              <div className="border-t border-gray-700 pb-3 pt-4">
                <div className="flex items-center px-5">
                  <div className="flex-shrink-0">
                    <div className="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                      QN
                    </div>
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium text-white">User</div>
                    <div className="text-sm font-medium text-gray-400">
                      {account ? shortenAddress(account) : ""}
                    </div>
                  </div>
                  <button
                    type="button"
                    className="ml-auto flex-shrink-0 rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                  >
                    <span className="sr-only">View notifications</span>
                    <BellIcon className="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>
                <div className="mt-3 space-y-1 px-2">
                  <DisclosureButton
                    as="a"
                    href="/profile"
                    className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                  >
                    Your Profile
                  </DisclosureButton>
                  <DisclosureButton
                    as="a"
                    href="/settings"
                    className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                  >
                    Settings
                  </DisclosureButton>
                  <DisclosureButton
                    as="button"
                    onClick={disconnectWallet}
                    className="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                  >
                    Disconnect Wallet
                  </DisclosureButton>
                  {isAuthenticated && (
                    <DisclosureButton
                      as="button"
                      onClick={logout}
                      className="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white"
                    >
                      Sign out
                    </DisclosureButton>
                  )}
                </div>
              </div>
            )}
          </DisclosurePanel>
        </>
      )}
    </Disclosure>
  );
}
