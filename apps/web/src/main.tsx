import { ClerkProvider } from "@clerk/clerk-react";
import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY as string;
const authDisabled = import.meta.env.VITE_AUTH_DISABLED === "true";

if (!authDisabled && !publishableKey) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY");
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {authDisabled ? (
      <App />
    ) : (
      <ClerkProvider publishableKey={publishableKey}>
        <App />
      </ClerkProvider>
    )}
  </React.StrictMode>
);
