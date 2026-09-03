"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { FormInput } from "@/components/ui/form-input";
export function LoginForm() {
  const router = useRouter();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const next: Record<string, string> = {};
    if (String(data.get("username") ?? "").trim().length < 3)
      next.username = "Use at least 3 characters.";
    if (String(data.get("password") ?? "").length < 8)
      next.password = "Use at least 8 characters.";
    setErrors(next);
    if (Object.keys(next).length) return;
    setLoading(true);
    window.setTimeout(() => router.push("/todos"), 650);
  }
  return (
    <form onSubmit={submit} noValidate className="grid gap-5">
      <div>
        <h2 className="font-display text-3xl font-semibold">Welcome back</h2>
        <p className="mt-1 text-sm text-muted">
          Any valid details work in this UI demo.
        </p>
      </div>
      <FormInput
        label="Username"
        name="username"
        autoComplete="username"
        placeholder="e.g. doni_dev"
        error={errors.username}
        required
      />
      <FormInput
        label="Password"
        name="password"
        type="password"
        autoComplete="current-password"
        placeholder="At least 8 characters"
        error={errors.password}
        required
      />
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Opening your day…" : "Log in"}
      </Button>
      <p className="text-center text-sm text-muted">
        New here?{" "}
        <Link
          className="font-bold text-ink underline decoration-accent decoration-2 underline-offset-4"
          href="/signup"
        >
          Create an account
        </Link>
      </p>
    </form>
  );
}
