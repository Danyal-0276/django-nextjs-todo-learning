import type { Metadata } from "next";
import { AuthShell } from "@/components/auth/auth-shell";
import { SignupForm } from "@/components/auth/signup-form";
export const metadata: Metadata = { title: "Sign up" };
export default function SignupPage() {
  return (
    <AuthShell
      eyebrow="Start with one small task"
      title="Build the habit. Learn the stack."
      copy="Create your account through the Django REST API, then log in to receive your JWT access and refresh tokens."
    >
      <SignupForm />
    </AuthShell>
  );
}
