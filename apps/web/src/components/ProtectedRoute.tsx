import { Navigate } from "react-router-dom";

import { useAuthState } from "../auth/useAuthState";

type Props = {
  children: JSX.Element;
};

export function ProtectedRoute({ children }: Props) {
  const { isLoaded, isSignedIn } = useAuthState();

  if (!isLoaded) {
    return <div>Loading authentication…</div>;
  }

  if (!isSignedIn) {
    return <Navigate to="/" replace />;
  }

  return children;
}
