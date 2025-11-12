'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '@/lib/firebase';
import { useStore } from '@/lib/store';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [firebaseUser, loading] = useAuthState(auth);
  const { setUser } = useStore();

  useEffect(() => {
    if (!loading) {
      if (firebaseUser) {
        setUser({
          uid: firebaseUser.uid,
          email: firebaseUser.email!,
          displayName: firebaseUser.displayName || undefined,
          photoURL: firebaseUser.photoURL || undefined,
          createdAt: new Date(firebaseUser.metadata.creationTime!),
        });
      } else {
        setUser(null);
      }
    }
  }, [firebaseUser, loading, setUser]);

  return <>{children}</>;
}

// Protected route wrapper
export function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const [user, loading] = useAuthState(auth);
    const router = useRouter();

    useEffect(() => {
      if (!loading && !user) {
        router.push('/login');
      }
    }, [user, loading, router]);

    if (loading) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        </div>
      );
    }

    if (!user) {
      return null;
    }

    return <Component {...props} />;
  };
}
