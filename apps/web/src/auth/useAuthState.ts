import { useAuth } from "@clerk/clerk-react";

export type AuthState = {
  isLoaded: boolean;
  isSignedIn: boolean;
  getToken: () => Promise<string | null>;
};

export function useAuthState(): AuthState {
  const { isLoaded, isSignedIn, getToken: clerkGetToken } = useAuth();

  const getToken = async () => {
    const cachedToken = await clerkGetToken();
    if (cachedToken) {
      return cachedToken;
    }

    return clerkGetToken({ skipCache: true });
  };

  return {
    isLoaded,
    isSignedIn: Boolean(isSignedIn),
    getToken
  };
}
