import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lead Management Dashboard",
  description: "A simple dashboard to view and manage classified leads",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}