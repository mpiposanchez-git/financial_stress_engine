import { useAuth } from "@clerk/clerk-react";

const authDisabled = import.meta.env.VITE_AUTH_DISABLED === "true";

export type AuthState = {
  isLoaded: boolean;
  isSignedIn: boolean;
  getToken: () => Promise<string | null>;
};

export function useAuthState(): AuthState {
  if (authDisabled) {
    return {
      isLoaded: true,
      isSignedIn: true,
      getToken: async () => null
    };
  }

  const { isLoaded, isSignedIn, getToken } = useAuth();

  return {
    isLoaded,
    isSignedIn: Boolean(isSignedIn),
    getToken
  };
}
