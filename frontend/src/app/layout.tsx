import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: { default: "Daymark", template: "%s · Daymark" }, description: "A mock todo frontend built to learn Next.js and Django REST integration." };
export default function RootLayout({ children }: LayoutProps<"/">) { return <html lang="en"><body>{children}</body></html>; }
