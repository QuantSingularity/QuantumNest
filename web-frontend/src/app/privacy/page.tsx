"use client";

import Link from "next/link";
import Navbar from "@/components/layout/Navbar";

const sections = [
  {
    title: "1. Information We Collect",
    content:
      "We collect information you provide directly (name, email, password), information generated through your use of the platform (portfolio data, transaction history, preferences), and technical information (IP address, browser type, device identifiers, usage data).",
  },
  {
    title: "2. How We Use Your Information",
    content:
      "We use your information to provide and improve our services, personalise your experience, send AI-generated investment recommendations, communicate updates and alerts, comply with legal obligations, and prevent fraud.",
  },
  {
    title: "3. Blockchain Data",
    content:
      "Blockchain transactions are inherently public. When you connect a wallet or execute on-chain transactions, your public address and transaction data may be visible on the blockchain. We do not control the public nature of blockchain data.",
  },
  {
    title: "4. Information Sharing",
    content:
      "We do not sell your personal information. We may share data with service providers who assist in operating the platform (subject to confidentiality obligations), when required by law, or in connection with a merger or acquisition. We may share anonymised, aggregated data for analytics.",
  },
  {
    title: "5. Data Retention",
    content:
      "We retain your personal data for as long as your account is active or as needed to provide services. You may request deletion of your account and associated data at any time, subject to legal retention requirements.",
  },
  {
    title: "6. Security",
    content:
      "We implement industry-standard security measures including encryption in transit and at rest, access controls, and regular security audits. However, no system is completely secure; you use the platform at your own risk.",
  },
  {
    title: "7. Cookies & Tracking",
    content:
      "We use cookies and similar technologies to maintain session state, remember preferences, and gather analytics. You may disable cookies in your browser, though some features may not function correctly.",
  },
  {
    title: "8. Your Rights",
    content:
      "Depending on your jurisdiction, you may have rights to access, correct, delete, or port your personal data; to object to or restrict certain processing; and to withdraw consent. Contact us at privacy@quantumnest.capital to exercise these rights.",
  },
  {
    title: "9. Children's Privacy",
    content:
      "The platform is not directed at individuals under 18. We do not knowingly collect personal information from children. If we learn we have collected data from a child, we will delete it promptly.",
  },
  {
    title: "10. Changes to This Policy",
    content:
      "We may update this Privacy Policy from time to time. We will notify you of material changes by posting a prominent notice on the platform or by email. Your continued use constitutes acceptance of the updated policy.",
  },
  {
    title: "11. Contact Us",
    content:
      "For privacy questions or concerns, contact our Data Protection Officer at privacy@quantumnest.capital or write to: QuantumNest Capital, Privacy Team, 100 Innovation Drive, San Francisco, CA 94105.",
  },
];

export default function Privacy() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="container mx-auto px-4 py-12 max-w-3xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
            Privacy Policy
          </h1>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            Last updated: April 1, 2025
          </p>
        </div>

        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-8">
          <p className="text-blue-800 dark:text-blue-300 text-sm">
            Your privacy matters to us. This policy explains what data we
            collect, how we use it, and the controls available to you.
          </p>
        </div>

        <div className="space-y-8">
          {sections.map((section) => (
            <section key={section.title}>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                {section.title}
              </h2>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {section.content}
              </p>
            </section>
          ))}
        </div>

        <div className="mt-12 pt-6 border-t border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row gap-4">
          <Link
            href="/terms"
            className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 font-medium"
          >
            Terms and Conditions →
          </Link>
          <Link
            href="/auth/register"
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 font-medium"
          >
            ← Back to Register
          </Link>
        </div>
      </main>
    </div>
  );
}
