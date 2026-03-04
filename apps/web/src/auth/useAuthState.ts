import { useAuth } from "@clerk/clerk-react";

export type AuthState = {
  isLoaded: boolean;
  isSignedIn: boolean;
  getToken: () => Promise<string | null>;
};

export function useAuthState(): AuthState {
  const { isLoaded, isSignedIn, getToken } = useAuth();

  return {
    isLoaded,
    isSignedIn: Boolean(isSignedIn),
    getToken
  };
}
