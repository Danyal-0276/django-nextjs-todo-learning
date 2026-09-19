"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { FormInput } from "@/components/ui/form-input";
import { ApiError } from "@/lib/api-client";
import { tokenStorage } from "@/lib/token-storage";
import { authService } from "@/services/auth-service";

export function LoginForm() {
  const router = useRouter();

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const data = new FormData(event.currentTarget);
    const username = String(data.get("username") ?? "").trim();
    const password = String(data.get("password") ?? "");
    const next: Record<string, string> = {};

    if (!username) {
      next.username = "Username is required.";
    }

    if (!password) {
      next.password = "Password is required.";
    }

    setErrors(next);

    if (Object.keys(next).length > 0) {
      return;
    }

    try {
      setLoading(true);

      const tokens = await authService.login({
        username,
        password,
      });

      tokenStorage.save(tokens);

      router.push("/todos");
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError) {
        setErrors({
          form: error.message,
        });
      } else {
        setErrors({
          form: "Could not connect to the server. Please try again.",
        });
      }
    } finally {
      setLoading(false);
    }
  }
  return (
    <form onSubmit={submit} noValidate className="grid gap-5">
      <div>
        <h2 className="font-display text-3xl font-semibold">Welcome back</h2>
        <p className="mt-1 text-sm text-muted">
          Enter the username and password registered with Django.
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
        placeholder="Enter your password"
        error={errors.password}
        required
      />
      {errors.form && (
        <p
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
        >
          {errors.form}
        </p>
      )}
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
