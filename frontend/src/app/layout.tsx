import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: { default: "Daymark", template: "%s · Daymark" },
  description:
    "A full-stack Todo application built with Next.js, Django REST Framework, PostgreSQL, and JWT authentication.",
};
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
