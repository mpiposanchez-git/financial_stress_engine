import { ClerkProvider } from "@clerk/clerk-react";
import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY as string;
const basePath = window.location.pathname.replace(/\/$/, "");
const appBasePath = basePath || "";
const postSignInUrl = `${appBasePath}/#/stress-test`;
const postSignOutUrl = `${appBasePath}/`;

if (!publishableKey) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY");
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider
      publishableKey={publishableKey}
      signInForceRedirectUrl={postSignInUrl}
      signInFallbackRedirectUrl={postSignInUrl}
      signUpForceRedirectUrl={postSignInUrl}
      signUpFallbackRedirectUrl={postSignInUrl}
      afterSignOutUrl={postSignOutUrl}
    >
      <App />
    </ClerkProvider>
  </React.StrictMode>
);
