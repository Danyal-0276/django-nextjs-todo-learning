"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/button";
import { FormInput } from "@/components/ui/form-input";
import { ApiError } from "@/lib/api-client";
import { authService } from "@/services/auth-service";

export function SignupForm() {
  const router = useRouter();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const next: Record<string, string> = {};
    const username = String(data.get("username") ?? "").trim();
    const email = String(data.get("email") ?? "").trim();
    const password = String(data.get("password") ?? "");
    const passwordConfirm = String(data.get("password_confirm") ?? "");
    if (String(data.get("username") ?? "").trim().length < 3)
      next.username = "Use at least 3 characters.";

    if (!/^\S+@\S+\.\S+$/.test(String(data.get("email") ?? "")))
      next.email = "Enter a valid email address.";

    if (String(data.get("password") ?? "").length < 8)
      next.password = "Use at least 8 characters.";
    if (password !== passwordConfirm) {
      next.password_confirm = "The passwords do not match.";
    }
    setErrors(next);

    if (Object.keys(next).length) return;

    try {
      setLoading(true);

      await authService.register({
        username,
        email,
        password,
        password_confirm: passwordConfirm,
      });

      router.push("/login");
    } catch (error) {
      if (error instanceof ApiError) {
        const apiErrors: Record<string, string> = {};

        for (const [field, messages] of Object.entries(error.data)) {
          const message = Array.isArray(messages) ? messages[0] : messages;

          if (field === "detail" || field === "non_field_errors") {
            apiErrors.form = message;
          } else {
            apiErrors[field] = message;
          }
        }

        if (Object.keys(apiErrors).length === 0) {
          apiErrors.form = error.message;
        }
        setErrors(apiErrors);
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
    <form onSubmit={submit} noValidate className="grid gap-4">
      <div>
        <h2 className="font-display text-3xl font-semibold">
          Create your space
        </h2>
        <p className="mt-1 text-sm text-muted">
          Your account will be created by the Django backend.
        </p>
      </div>
      <FormInput
        label="Username"
        name="username"
        autoComplete="username"
        placeholder="Choose a username"
        error={errors.username}
        required
      />
      <FormInput
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        placeholder="you@example.com"
        error={errors.email}
        required
      />
      <FormInput
        label="Password"
        name="password"
        type="password"
        autoComplete="new-password"
        placeholder="At least 8 characters"
        error={errors.password}
        required
      />
      <FormInput
        label="Confirm password"
        name="password_confirm"
        type="password"
        autoComplete="new-password"
        placeholder="Enter the password again"
        error={errors.password_confirm}
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
      <Button type="submit" disabled={loading} className="mt-1 w-full">
        {loading ? "Creating your space…" : "Create account"}
      </Button>
      <p className="text-center text-sm text-muted">
        Already have an account?{" "}
        <Link
          className="font-bold text-ink underline decoration-accent decoration-2 underline-offset-4"
          href="/login"
        >
          Log in
        </Link>
      </p>
    </form>
  );
}
