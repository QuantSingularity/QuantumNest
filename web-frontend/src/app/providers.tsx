"use client";

import { ApiProvider } from "@/lib/api";
import { BlockchainProvider } from "@/lib/blockchain";
import { AuthProvider } from "./auth/AuthContext";

// FIXED: ApiProvider must wrap AuthProvider because AuthProvider calls useApi() internally.
// Previous order had AuthProvider as the outermost wrapper which caused a crash.
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ApiProvider>
      <AuthProvider>
        <BlockchainProvider>{children}</BlockchainProvider>
      </AuthProvider>
    </ApiProvider>
  );
}
