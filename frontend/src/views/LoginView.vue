<template>
  <div class="auth-container">
    <div class="form-container">
      <!-- Form Wrapper -->
      <div class="form-wrapper">
        <!-- Login Form - Made visible by default -->
        <div class="form-panel" :class="{ 'active': !isSignupMode }">
          <div class="form-content">
            <div class="form-header">
              <h2>Welcome Back</h2>
              <p class="form-subtitle">Sign in to continue</p>
            </div>
            
            <p v-if="error" class="error-message">{{ error }}</p>
            
            <form @submit.prevent="login">
              <div class="form-group">
                <div class="input-container" :class="{ 'input-focus': usernameFocused || username.length > 0 }">
                  <label for="username">Username</label>
                  <input 
                    id="username"
                    v-model="username" 
                    type="text" 
                    required
                    @focus="usernameFocused = true"
                    @blur="usernameFocused = false"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <div class="input-container" :class="{ 'input-focus': passwordFocused || password.length > 0 }">
                  <label for="password">Password</label>
                  <input 
                    id="password"
                    v-model="password" 
                    type="password" 
                    required
                    @focus="passwordFocused = true"
                    @blur="passwordFocused = false"
                  >
                </div>
              </div>
              
              <button type="submit" class="btn-primary" :disabled="isLoading">
                {{ isLoading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            
            <div class="form-footer">
              <p>Don't have an account?</p>
              <button @click="switchMode" class="btn-switch">Sign Up</button>
            </div>
          </div>
        </div>
        
        <!-- Sign Up Form -->
        <div class="form-panel" :class="{ 'active': isSignupMode }">
          <div class="form-content">
            <div class="form-header">
              <h2>Create Account</h2>
              <p class="form-subtitle">Join our community</p>
            </div>
            
            <p v-if="signupError" class="error-message">{{ signupError }}</p>
            
            <form @submit.prevent="signUp">
              <div class="form-group">
                <div class="input-container" :class="{ 'input-focus': signupUsernameFocused || signupUsername.length > 0 }">
                  <label for="signup-username">Username</label>
                  <input 
                    id="signup-username"
                    v-model="signupUsername" 
                    type="text" 
                    required
                    @focus="signupUsernameFocused = true"
                    @blur="signupUsernameFocused = false"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <div class="input-container" :class="{ 'input-focus': signupPasswordFocused || signupPassword.length > 0 }">
                  <label for="signup-password">Password</label>
                  <input 
                    id="signup-password"
                    v-model="signupPassword" 
                    type="password" 
                    required
                    @focus="signupPasswordFocused = true"
                    @blur="signupPasswordFocused = false"
                  >
                </div>
              </div>
              
              <div class="form-group">
                <div class="input-container" :class="{ 'input-focus': confirmPasswordFocused || confirmPassword.length > 0 }">
                  <label for="confirm-password">Confirm Password</label>
                  <input 
                    id="confirm-password"
                    v-model="confirmPassword" 
                    type="password" 
                    required
                    @focus="confirmPasswordFocused = true"
                    @blur="confirmPasswordFocused = false"
                  >
                </div>
              </div>
              
              <button type="submit" class="btn-primary" :disabled="isSigningUp">
                {{ isSigningUp ? 'Creating account...' : 'Sign Up' }}
              </button>
            </form>
            
            <div class="form-footer">
              <p>Already have an account?</p>
              <button @click="switchMode" class="btn-switch">Login</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Background animated elements -->
    <div class="animated-background">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      <div class="circle circle-4"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRoute, useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

// Mode switch control
const isSignupMode = ref(false);

// Login Form data
const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);
const usernameFocused = ref(false);
const passwordFocused = ref(false);

// Sign Up Form data
const signupUsername = ref('');
const signupPassword = ref('');
const confirmPassword = ref('');
const signupError = ref('');
const isSigningUp = ref(false);
const signupUsernameFocused = ref(false);
const signupPasswordFocused = ref(false);
const confirmPasswordFocused = ref(false);

// Switch between login and signup modes
const switchMode = () => {
  isSignupMode.value = !isSignupMode.value;
  error.value = '';
  signupError.value = '';
};

// Login function
const login = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password';
    return;
  }

  try {
    isLoading.value = true;
    error.value = '';
    
    await authStore.login(username.value, password.value);
    
    const redirectPath = route.query.redirect as string || '/';
    router.push(redirectPath);
  } catch (err) {
    error.value = err instanceof Error 
      ? err.message 
      : 'Failed to login. Please check your credentials and try again.';
  } finally {
    isLoading.value = false;
  }
};

// Sign Up function
const signUp = async () => {
  if (!signupUsername.value || !signupPassword.value || !confirmPassword.value) {
    signupError.value = 'Please fill in all fields';
    return;
  }

  if (signupPassword.value !== confirmPassword.value) {
    signupError.value = 'Passwords do not match';
    return;
  }

  try {
    isSigningUp.value = true;
    signupError.value = '';
    
    await authStore.signUp(signupUsername.value, signupPassword.value);

    const redirectPath = route.query.redirect as string || '/';
    router.push(redirectPath);
  } catch (err) {
    signupError.value = err instanceof Error 
      ? err.message 
      : 'Failed to sign up. Please try again.';
  } finally {
    isSigningUp.value = false;
  }
};

onMounted(() => {
  switchMode()
  setTimeout(() => switchMode(), 100)
})
</script>

<style>
:root {
  --primary-color: #00ccff; /* Bright cyan */
  --secondary-color: #ff00ff; /* Bright magenta */
  --accent-color: #ffcc00; /* Bright yellow */
  --bg-color: #ffffff; /* White background */
  --card-bg: rgba(255, 255, 255, 0.9); /* White with opacity */
  --text-color: #333333; /* Dark gray for text */
  --text-light: #666666; /* Medium gray for lighter text */
  --error-color: #ff3333; /* Bright red */
  --success-color: #33cc33; /* Bright green */
  --input-border: rgba(0, 0, 0, 0.1);
  --button-text: #ffffff; /* White text for buttons */
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa, #e4e9f2);
  position: relative;
  overflow: hidden;
}

/* Animated background */
.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  filter: blur(40px);
}

.circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.5;
  animation: float 15s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: var(--primary-color);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 400px;
  height: 400px;
  background: var(--secondary-color);
  top: 70%;
  right: -150px;
  animation-delay: -2s;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: var(--accent-color);
  bottom: -80px;
  left: 30%;
  animation-delay: -5s;
}

.circle-4 {
  width: 250px;
  height: 250px;
  background: var(--primary-color);
  top: 20%;
  right: 20%;
  animation-delay: -8s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-20px) translateX(20px);
  }
  50% {
    transform: translateY(10px) translateX(-15px);
  }
  75% {
    transform: translateY(15px) translateX(10px);
  }
}

/* Form container */
.form-container {
  position: relative;
  width: 90%;
  max-width: 450px;
  height: 90%;
  min-height: 500px;
  z-index: 1;
}

.form-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.form-panel {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  visibility: hidden;
  transform: translateX(-20px);
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0.5s;
  backface-visibility: hidden;
}

.form-panel.active {
  width: 100%;
  height: 100%;
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
  z-index: 2;
}

.form-content {
  width: 100%;
  padding: 2.5rem;
  border-radius: 16px;
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  color: var(--text-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.form-content:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15), 
              0 0 20px rgba(0, 204, 255, 0.3);
  transform: translateY(-5px);
}

/* Form header */
.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-subtitle {
  color: var(--text-light);
  font-size: 1rem;
}

/* Form elements */
form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  position: relative;
}

.input-container {
  position: relative;
  margin-bottom: 0.5rem;
}

label {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  pointer-events: none;
  transition: all 0.3s ease;
  font-size: 1rem;
  background-color: transparent;
  padding: 0 0.25rem;
  z-index: 1;
}

.input-container.input-focus label {
  top: 0;
  transform: translateY(-50%);
  font-size: 0.75rem;
  color: var(--primary-color);
  background-color: var(--card-bg);
}

input {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid var(--input-border);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  color: var(--text-color);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 10px rgba(0, 204, 255, 0.4);
}

/* Buttons */
.btn-primary {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  color: var(--button-text);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 204, 255, 0.5);
  margin-top: 1rem;
}

.btn-primary:hover {
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  box-shadow: 0 6px 16px rgba(0, 204, 255, 0.7);
  transform: translateY(-2px);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 204, 255, 0.5);
}

.btn-primary:disabled {
  background: rgba(200, 200, 200, 0.7);
  color: rgba(100, 100, 100, 0.7);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
}

.btn-primary:hover::before {
  width: 300px;
  height: 300px;
}

/* Form footer */
.form-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
  color: var(--text-light);
  font-size: 0.875rem;
}

.btn-switch {
  background: none;
  border: none;
  color: var(--primary-color);
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-switch:hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

/* Error messages */
.error-message {
  color: var(--error-color);
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.875rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: rgba(255, 51, 51, 0.1);
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .form-content {
    padding: 1.5rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
}
</style>
