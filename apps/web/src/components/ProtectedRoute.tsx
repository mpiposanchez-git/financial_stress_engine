import { Navigate } from "react-router-dom";

import { useAuthState } from "../auth/useAuthState";

const authDisabled = import.meta.env.VITE_AUTH_DISABLED === "true";

type Props = {
  children: JSX.Element;
};

export function ProtectedRoute({ children }: Props) {
  if (authDisabled) {
    return children;
  }

  const { isLoaded, isSignedIn } = useAuthState();

  if (!isLoaded) {
    return <div>Loading authentication…</div>;
  }

  if (!isSignedIn) {
    return <Navigate to="/" replace />;
  }

  return children;
}
