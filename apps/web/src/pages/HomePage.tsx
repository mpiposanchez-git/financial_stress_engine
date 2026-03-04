import {
  SignInButton,
  SignOutButton,
  useAuth,
  useSignIn
} from "@clerk/clerk-react";
import { Link } from "react-router-dom";

export function HomePage() {
  const { isLoaded: isAuthLoaded, isSignedIn } = useAuth();
  const { isLoaded: isSignInLoaded, signIn } = useSignIn();

  const isReady = isAuthLoaded && isSignInLoaded;

  const onGitHubSignIn = async () => {
    if (!isReady || !signIn) {
      return;
    }

    await signIn.authenticateWithRedirect({
      strategy: "oauth_github",
      redirectUrl: window.location.href,
      redirectUrlComplete: window.location.href
    });
  };

  return (
    <main>
      <h1>UK Household Financial Stress Simulation</h1>
      <p>
        This tool provides illustrative simulation outputs only. It is not financial advice,
        investment advice, or product recommendation.
      </p>
      {!isReady ? <p>Loading authentication…</p> : null}
      {isReady && !isSignedIn ? (
        <>
          <button type="button" onClick={() => void onGitHubSignIn()}>
            Sign in with GitHub
          </button>
          <SignInButton mode="redirect">
            <button type="button">Sign in</button>
          </SignInButton>
        </>
      ) : null}
      {isReady && isSignedIn ? (
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
