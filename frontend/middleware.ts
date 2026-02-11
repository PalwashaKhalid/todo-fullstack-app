import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;

  // Protected routes that require authentication
  const protectedRoutes = ['/dashboard'];
  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));

  // Check if user is trying to access protected route without token
  if (isProtectedRoute && !token) {
    // Check localStorage via client-side (this is a fallback)
    // Since middleware runs on server, we redirect to login
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Redirect authenticated users away from auth pages
  const authRoutes = ['/login', '/signup'];
  const isAuthRoute = authRoutes.includes(pathname);

  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup'],
};
