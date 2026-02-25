import { AuthProvider } from "@/components/AuthProvider";
import "@/app/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CropSense AI | Hyper-local Crop Advisor",
  description: "Detect crop diseases, get treatment advisory, and predict 48-hour spread risk.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen antialiased">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
