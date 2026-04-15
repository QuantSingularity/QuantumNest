"use client";

import Link from "next/link";
import Navbar from "@/components/layout/Navbar";

const sections = [
  {
    title: "1. Acceptance of Terms",
    content:
      "By accessing or using the QuantumNest Capital platform, you agree to be bound by these Terms and Conditions. If you do not agree to these terms, please do not use our services. These terms apply to all visitors, users, and others who access the platform.",
  },
  {
    title: "2. Description of Service",
    content:
      "QuantumNest Capital is an AI-powered tokenized asset investment platform that integrates artificial intelligence, blockchain technology, data science, and automation tools. We provide portfolio management, market analysis, AI-driven recommendations, and blockchain explorer features.",
  },
  {
    title: "3. User Accounts",
    content:
      "To access certain features you must create an account. You are responsible for maintaining the confidentiality of your credentials and for all activities that occur under your account. You must notify us immediately of any unauthorized use. We reserve the right to terminate accounts at our discretion.",
  },
  {
    title: "4. Investment Disclaimer",
    content:
      "QuantumNest Capital does not provide financial, investment, legal, or tax advice. All content is for informational purposes only. Past performance is not indicative of future results. Investments involve risk, including possible loss of principal. You should consult a licensed financial advisor before making investment decisions.",
  },
  {
    title: "5. Blockchain & Wallet Services",
    content:
      "Our platform integrates with third-party wallet providers (such as MetaMask). We are not responsible for losses arising from wallet compromise, smart contract bugs, or blockchain network issues. You are solely responsible for securing your private keys and wallet credentials.",
  },
  {
    title: "6. Prohibited Uses",
    content:
      "You may not use the platform for any unlawful purpose, to transmit harmful or fraudulent content, to interfere with platform security, to engage in market manipulation, or to violate any applicable laws or regulations including securities laws.",
  },
  {
    title: "7. Intellectual Property",
    content:
      "All content, features, and functionality of the platform — including but not limited to text, graphics, logos, and software — are the exclusive property of QuantumNest Capital and are protected by intellectual property laws.",
  },
  {
    title: "8. Limitation of Liability",
    content:
      "To the fullest extent permitted by law, QuantumNest Capital shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising from your use of the platform, even if we have been advised of the possibility of such damages.",
  },
  {
    title: "9. Changes to Terms",
    content:
      "We reserve the right to modify these terms at any time. We will notify users of significant changes by posting a notice on the platform. Continued use after changes constitutes acceptance of the new terms.",
  },
  {
    title: "10. Contact",
    content:
      "If you have questions about these Terms and Conditions, please contact us at legal@quantumnest.capital.",
  },
];

export default function Terms() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="container mx-auto px-4 py-12 max-w-3xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
            Terms and Conditions
          </h1>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            Last updated: April 1, 2025
          </p>
        </div>

        <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 mb-8">
          <p className="text-amber-800 dark:text-amber-300 text-sm">
            <strong>Important:</strong> Please read these terms carefully before
            using the QuantumNest Capital platform. These constitute a legally
            binding agreement between you and QuantumNest Capital.
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
            href="/privacy"
            className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 font-medium"
          >
            Privacy Policy →
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
