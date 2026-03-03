import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { ProtectedRoute } from "./ProtectedRoute";

vi.mock("../auth/useAuthState", () => ({
  useAuthState: () => ({
    isLoaded: true,
    isSignedIn: false,
    getToken: vi.fn()
  })
}));

describe("ProtectedRoute", () => {
  it("denies unauthenticated access", () => {
    render(
      <MemoryRouter initialEntries={["/stress-test", "/"]}>
        <Routes>
          <Route path="/" element={<div>Home</div>} />
          <Route
            path="/stress-test"
            element={
              <ProtectedRoute>
                <div>Protected</div>
              </ProtectedRoute>
            }
          />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.queryByText("Protected")).not.toBeInTheDocument();
  });
});
