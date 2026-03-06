import { SignedIn, SignedOut, SignInButton, SignOutButton } from "@clerk/clerk-react";
import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <main>
      <h1>UK Household Financial Stress Simulation</h1>
      <p>
        This tool provides illustrative simulation outputs only. It is not financial advice,
        investment advice, or product recommendation.
      </p>
      <SignedOut>
        <SignInButton mode="modal">
          <button type="button">Sign in</button>
        </SignInButton>
      </SignedOut>
      <SignedIn>
        <SignOutButton>
          <button type="button">Sign out</button>
        </SignOutButton>
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
          <li>
            <Link to="/data-sources">Data Sources</Link>
          </li>
        </ul>
      </nav>
    </main>
  );
}
