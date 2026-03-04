import {
  SignInButton,
  SignOutButton,
  useAuth
} from "@clerk/clerk-react";
import { Link } from "react-router-dom";

export function HomePage() {
  const { isLoaded: isAuthLoaded, isSignedIn } = useAuth();

  return (
    <main>
      <h1>UK Household Financial Stress Simulation</h1>
      <p>
        This tool provides illustrative simulation outputs only. It is not financial advice,
        investment advice, or product recommendation.
      </p>
      {!isAuthLoaded ? <p>Loading authentication…</p> : null}
      {isAuthLoaded && !isSignedIn ? (
        <SignInButton mode="redirect">
          <button type="button">Sign in</button>
        </SignInButton>
      ) : null}
      {isAuthLoaded && isSignedIn ? (
        <SignOutButton>
          <button type="button">Sign out</button>
        </SignOutButton>
      ) : null}
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
