import { SignedIn, SignedOut, SignInButton, SignOutButton } from "@clerk/clerk-react";
import { Link } from "react-router-dom";

const authDisabled = import.meta.env.VITE_AUTH_DISABLED === "true";

export function HomePage() {
  return (
    <main>
      <h1>UK Household Financial Stress Simulation</h1>
      <p>
        This tool provides illustrative simulation outputs only. It is not financial advice,
        investment advice, or product recommendation.
      </p>
      {authDisabled ? <p>Authentication disabled for diagnostics.</p> : null}
      <SignedOut>
        {authDisabled ? null : (
          <SignInButton mode="modal">
            <button type="button">Sign in</button>
          </SignInButton>
        )}
      </SignedOut>
      <SignedIn>
        {authDisabled ? null : (
          <SignOutButton>
            <button type="button">Sign out</button>
          </SignOutButton>
        )}
      </SignedIn>
      <nav>
        <ul>
          <li>
            <Link to="/stress-test">Stress Test</Link>
          </li>
          <li>
            <Link to="/results">Results</Link>
          </li>
          <li>
            <Link to="/about">About / Disclaimer</Link>
          </li>
        </ul>
      </nav>
    </main>
  );
}
