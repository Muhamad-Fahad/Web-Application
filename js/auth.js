/**
 * Authentication and Session Management
 * CyberTech Identity & Access System
 */

const AUTH_KEY = 'cyber_auth_session';

const Auth = {
  // Check if session exists
  isAuthenticated() {
    try {
      const session = localStorage.getItem(AUTH_KEY);
      return !!session && JSON.parse(session).isLoggedIn === true;
    } catch (e) {
      return false;
    }
  },

  // Get current user details
  getCurrentUser() {
    try {
      const session = localStorage.getItem(AUTH_KEY);
      return session ? JSON.parse(session) : null;
    } catch (e) {
      return null;
    }
  },

  // Log in user
  login(email, role = 'Security Specialist') {
    const username = email.split('@')[0];
    const sessionData = {
      isLoggedIn: true,
      email: email,
      username: username.charAt(0).toUpperCase() + username.slice(1),
      role: role,
      token: 'SEC-TOKEN-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
      loginTime: new Date().toISOString()
    };
    localStorage.setItem(AUTH_KEY, JSON.stringify(sessionData));
    return sessionData;
  },

  // Log out user
  logout() {
    localStorage.removeItem(AUTH_KEY);
    window.location.href = 'index.html';
  },

  // Route protection
  protectPage(pageType) {
    const isAuth = this.isAuthenticated();

    if (pageType === 'private' && !isAuth) {
      // Trying to access dashboard without login
      window.location.href = 'index.html?redirect=unauthorized';
    } else if (pageType === 'public' && isAuth) {
      // Already logged in trying to access login page
      window.location.href = 'dashboard.html';
    }
  }
};

// Expose globally
window.Auth = Auth;
