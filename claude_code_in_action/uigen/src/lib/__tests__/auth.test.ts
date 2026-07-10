// @vitest-environment node
import { describe, it, expect, vi, beforeEach } from "vitest";
import { jwtVerify } from "jose";

const setMock = vi.fn();

vi.mock("server-only", () => ({}));

vi.mock("next/headers", () => ({
  cookies: vi.fn(async () => ({
    set: setMock,
  })),
}));

import { createSession } from "@/lib/auth";

const JWT_SECRET = new TextEncoder().encode(
  process.env.JWT_SECRET || "development-secret-key"
);

describe("createSession", () => {
  beforeEach(() => {
    setMock.mockClear();
  });

  it("sets an auth-token cookie", async () => {
    await createSession("user-1", "user@example.com");

    expect(setMock).toHaveBeenCalledTimes(1);
    const [name, token, options] = setMock.mock.calls[0];
    expect(name).toBe("auth-token");
    expect(typeof token).toBe("string");
    expect(options).toMatchObject({
      httpOnly: true,
      sameSite: "lax",
      path: "/",
    });
    expect(options.expires).toBeInstanceOf(Date);
  });

  it("signs a JWT containing the userId and email", async () => {
    await createSession("user-1", "user@example.com");

    const [, token] = setMock.mock.calls[0];
    const { payload } = await jwtVerify(token, JWT_SECRET);

    expect(payload.userId).toBe("user-1");
    expect(payload.email).toBe("user@example.com");
    expect(payload.expiresAt).toBeDefined();
  });

  it("sets an expiration roughly 7 days in the future", async () => {
    const before = Date.now();
    await createSession("user-1", "user@example.com");
    const after = Date.now();

    const [, , options] = setMock.mock.calls[0];
    const expiresAt = options.expires.getTime();

    const sevenDays = 7 * 24 * 60 * 60 * 1000;
    expect(expiresAt).toBeGreaterThanOrEqual(before + sevenDays - 5000);
    expect(expiresAt).toBeLessThanOrEqual(after + sevenDays + 5000);
  });

  it("marks the cookie secure only in production", async () => {
    const originalEnv = process.env.NODE_ENV;

    (process.env as any).NODE_ENV = "development";
    await createSession("user-1", "user@example.com");
    expect(setMock.mock.calls[0][2].secure).toBe(false);

    setMock.mockClear();

    (process.env as any).NODE_ENV = "production";
    await createSession("user-1", "user@example.com");
    expect(setMock.mock.calls[0][2].secure).toBe(true);

    (process.env as any).NODE_ENV = originalEnv;
  });
});
