import { describe, test, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";
import { useAuth } from "@/hooks/use-auth";
import { signIn as signInAction, signUp as signUpAction } from "@/actions";
import { getAnonWorkData, clearAnonWork } from "@/lib/anon-work-tracker";
import { getProjects } from "@/actions/get-projects";
import { createProject } from "@/actions/create-project";

const pushMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}));

vi.mock("@/actions", () => ({
  signIn: vi.fn(),
  signUp: vi.fn(),
}));

vi.mock("@/lib/anon-work-tracker", () => ({
  getAnonWorkData: vi.fn(),
  clearAnonWork: vi.fn(),
}));

vi.mock("@/actions/get-projects", () => ({
  getProjects: vi.fn(),
}));

vi.mock("@/actions/create-project", () => ({
  createProject: vi.fn(),
}));

describe("useAuth", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (getAnonWorkData as any).mockReturnValue(null);
    (getProjects as any).mockResolvedValue([]);
  });

  describe("signIn", () => {
    test("returns the action result on success", async () => {
      (signInAction as any).mockResolvedValue({ success: true });
      (getProjects as any).mockResolvedValue([{ id: "proj-1" }]);

      const { result } = renderHook(() => useAuth());

      let signInResult: any;
      await act(async () => {
        signInResult = await result.current.signIn("a@b.com", "password");
      });

      expect(signInAction).toHaveBeenCalledWith("a@b.com", "password");
      expect(signInResult).toEqual({ success: true });
    });

    test("returns the action result on failure and does not navigate", async () => {
      (signInAction as any).mockResolvedValue({
        success: false,
        error: "Invalid credentials",
      });

      const { result } = renderHook(() => useAuth());

      let signInResult: any;
      await act(async () => {
        signInResult = await result.current.signIn("a@b.com", "wrong");
      });

      expect(signInResult).toEqual({
        success: false,
        error: "Invalid credentials",
      });
      expect(pushMock).not.toHaveBeenCalled();
      expect(getAnonWorkData).not.toHaveBeenCalled();
    });

    test("sets isLoading true while pending and false after completion", async () => {
      let resolveSignIn: (value: any) => void;
      (signInAction as any).mockReturnValue(
        new Promise((resolve) => {
          resolveSignIn = resolve;
        })
      );
      (createProject as any).mockResolvedValue({ id: "brand-new-project" });

      const { result } = renderHook(() => useAuth());

      expect(result.current.isLoading).toBe(false);

      let signInPromise: Promise<any>;
      act(() => {
        signInPromise = result.current.signIn("a@b.com", "password");
      });

      await waitFor(() => expect(result.current.isLoading).toBe(true));

      await act(async () => {
        resolveSignIn!({ success: true });
        await signInPromise;
      });

      expect(result.current.isLoading).toBe(false);
    });

    test("resets isLoading even if the action throws", async () => {
      (signInAction as any).mockRejectedValue(new Error("network error"));

      const { result } = renderHook(() => useAuth());

      await act(async () => {
        await expect(
          result.current.signIn("a@b.com", "password")
        ).rejects.toThrow("network error");
      });

      expect(result.current.isLoading).toBe(false);
    });

    describe("post sign-in redirect behavior", () => {
      test("creates a project from anonymous work and navigates to it, clearing anon work", async () => {
        (signInAction as any).mockResolvedValue({ success: true });
        (getAnonWorkData as any).mockReturnValue({
          messages: [{ id: "1", role: "user", content: "hi" }],
          fileSystemData: { "/App.jsx": { type: "file", content: "" } },
        });
        (createProject as any).mockResolvedValue({ id: "new-anon-project" });

        const { result } = renderHook(() => useAuth());

        await act(async () => {
          await result.current.signIn("a@b.com", "password");
        });

        expect(createProject).toHaveBeenCalledWith(
          expect.objectContaining({
            messages: [{ id: "1", role: "user", content: "hi" }],
            data: { "/App.jsx": { type: "file", content: "" } },
          })
        );
        expect(clearAnonWork).toHaveBeenCalled();
        expect(pushMock).toHaveBeenCalledWith("/new-anon-project");
        expect(getProjects).not.toHaveBeenCalled();
      });

      test("ignores anonymous work with no messages and falls back to existing projects", async () => {
        (signInAction as any).mockResolvedValue({ success: true });
        (getAnonWorkData as any).mockReturnValue({
          messages: [],
          fileSystemData: {},
        });
        (getProjects as any).mockResolvedValue([{ id: "existing-project" }]);

        const { result } = renderHook(() => useAuth());

        await act(async () => {
          await result.current.signIn("a@b.com", "password");
        });

        expect(createProject).not.toHaveBeenCalled();
        expect(pushMock).toHaveBeenCalledWith("/existing-project");
      });

      test("navigates to the most recent existing project when there is no anon work", async () => {
        (signInAction as any).mockResolvedValue({ success: true });
        (getProjects as any).mockResolvedValue([
          { id: "project-a" },
          { id: "project-b" },
        ]);

        const { result } = renderHook(() => useAuth());

        await act(async () => {
          await result.current.signIn("a@b.com", "password");
        });

        expect(pushMock).toHaveBeenCalledWith("/project-a");
        expect(createProject).not.toHaveBeenCalled();
      });

      test("creates a new empty project when there is no anon work and no existing projects", async () => {
        (signInAction as any).mockResolvedValue({ success: true });
        (getProjects as any).mockResolvedValue([]);
        (createProject as any).mockResolvedValue({ id: "brand-new-project" });

        const { result } = renderHook(() => useAuth());

        await act(async () => {
          await result.current.signIn("a@b.com", "password");
        });

        expect(createProject).toHaveBeenCalledWith(
          expect.objectContaining({
            messages: [],
            data: {},
          })
        );
        expect(pushMock).toHaveBeenCalledWith("/brand-new-project");
      });
    });
  });

  describe("signUp", () => {
    test("returns the action result on success", async () => {
      (signUpAction as any).mockResolvedValue({ success: true });
      (getProjects as any).mockResolvedValue([{ id: "proj-1" }]);

      const { result } = renderHook(() => useAuth());

      let signUpResult: any;
      await act(async () => {
        signUpResult = await result.current.signUp("a@b.com", "password");
      });

      expect(signUpAction).toHaveBeenCalledWith("a@b.com", "password");
      expect(signUpResult).toEqual({ success: true });
    });

    test("returns the action result on failure and does not navigate", async () => {
      (signUpAction as any).mockResolvedValue({
        success: false,
        error: "Email already in use",
      });

      const { result } = renderHook(() => useAuth());

      let signUpResult: any;
      await act(async () => {
        signUpResult = await result.current.signUp("a@b.com", "password");
      });

      expect(signUpResult).toEqual({
        success: false,
        error: "Email already in use",
      });
      expect(pushMock).not.toHaveBeenCalled();
    });

    test("sets isLoading true while pending and false after completion", async () => {
      let resolveSignUp: (value: any) => void;
      (signUpAction as any).mockReturnValue(
        new Promise((resolve) => {
          resolveSignUp = resolve;
        })
      );

      const { result } = renderHook(() => useAuth());

      let signUpPromise: Promise<any>;
      act(() => {
        signUpPromise = result.current.signUp("a@b.com", "password");
      });

      await waitFor(() => expect(result.current.isLoading).toBe(true));

      await act(async () => {
        resolveSignUp!({ success: true });
        await signUpPromise;
      });

      expect(result.current.isLoading).toBe(false);
    });

    test("resets isLoading even if the action throws", async () => {
      (signUpAction as any).mockRejectedValue(new Error("network error"));

      const { result } = renderHook(() => useAuth());

      await act(async () => {
        await expect(
          result.current.signUp("a@b.com", "password")
        ).rejects.toThrow("network error");
      });

      expect(result.current.isLoading).toBe(false);
    });

    test("creates a project from anonymous work on successful sign-up", async () => {
      (signUpAction as any).mockResolvedValue({ success: true });
      (getAnonWorkData as any).mockReturnValue({
        messages: [{ id: "1", role: "user", content: "hi" }],
        fileSystemData: { "/App.jsx": { type: "file", content: "" } },
      });
      (createProject as any).mockResolvedValue({ id: "new-anon-project" });

      const { result } = renderHook(() => useAuth());

      await act(async () => {
        await result.current.signUp("a@b.com", "password");
      });

      expect(clearAnonWork).toHaveBeenCalled();
      expect(pushMock).toHaveBeenCalledWith("/new-anon-project");
    });
  });
});
