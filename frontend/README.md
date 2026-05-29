# HSE Management System - Frontend

Modern, responsive frontend application for HSE (Health, Safety & Environment) management system built with Vue 3, Vite, and Tailwind CSS.

## 🎯 Overview

Comprehensive web application for offshore vessel HSE operations with real-time monitoring, permit-to-work management, incident reporting, and analytics dashboard.

### Key Features
- ✅ **JWT Authentication**: Secure token-based authentication with role-based access
- ✅ **Dark Mode Support**: Full light/dark theme with persistent preference
- ✅ **Real-time Updates**: WebSocket integration for live dashboard
- ✅ **Responsive Design**: Mobile-first, works on all devices
- ✅ **Role-Based UI**: Different views for Worker, Safety Officer, Admin
- ✅ **PTW Management**: Complete workflow from submission to closure
- ✅ **POB Tracking**: Live personnel location tracking with visual map
- ✅ **Incident Reporting**: Comprehensive incident reporting with proof upload
- ✅ **Analytics Dashboard**: Charts, trends, compliance reports, location hotspots
- ✅ **Asset Management**: Asset tracking and maintenance scheduling
- ✅ **Modern UI**: Reka UI components with Tailwind CSS v4

---

## 🛠️ Tech Stack

- **Framework**: Vue 3.5+ (Composition API with `<script setup>`)
- **Build Tool**: Vite 8.0+
- **UI Library**: Reka UI (Headless UI components)
- **Styling**: Tailwind CSS v4 with CSS custom properties
- **State Management**: Reactive stores (theme, auth, vessel, websocket)
- **HTTP Client**: Fetch API with JWT authentication
- **Charts**: Chart.js 4.5+ with vue-chartjs
- **Data Tables**: TanStack Vue Table 8.21+
- **Notifications**: Vue Sonner
- **Icons**: Lucide Vue
- **Router**: Vue Router 4.6+
- **Utilities**: VueUse Core 14.3+

---

## 📦 Installation

### Prerequisites
- Node.js 18.0 or higher
- npm or yarn
- Backend API running on `http://localhost:8989`

### Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8989/api/v1
VITE_WS_URL=ws://localhost:8989/ws/pob/
EOF

# Start development server
npm run dev
```

Access at: `http://localhost:5173`

### Default Test Users
After running backend seed command, you can login with:

**Admin**:
- Username: `admin`
- Password: `admin123`

**Safety Officer**:
- Username: `safety_officer`
- Password: `safety123`

**Worker**:
- Username: `worker`
- Password: `worker123`

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/                # Reusable components
│   │   ├── analytics/            # Analytics tab components
│   │   │   ├── SafetyMetricsTab.vue
│   │   │   ├── IncidentTrendsTab.vue
│   │   │   ├── ComplianceReportsTab.vue
│   │   │   ├── LocationHotspotsTab.vue
│   │   │   └── ConditionChangeAuditTab.vue
│   │   │
│   │   ├── DashboardStats.vue    # Main metrics display
│   │   ├── PobVisualMap.vue      # Location tracking map
│   │   ├── IncidentReportForm.vue # Incident reporting form
│   │   ├── PtwModal.vue          # PTW workflow modal
│   │   ├── WaitingForClose.vue   # PTW waiting for close state
│   │   ├── PendingApprovals.vue  # Safety officer approvals
│   │   ├── WorkerDashboard.vue   # Worker-specific dashboard
│   │   ├── Login.vue             # Login form component
│   │   ├── QuickLogin.vue        # Quick login for testing
│   │   └── LogoutConfirmModal.vue # Logout confirmation
│   │
│   ├── views/                    # Page components (routes)
│   │   ├── DashboardView.vue     # Main dashboard
│   │   ├── AdminDashboardView.vue # Admin-specific dashboard
│   │   ├── PtwView.vue           # PTW management with data table
│   │   ├── IncidentsView.vue     # Incident management
│   │   ├── AnalyticsView.vue     # Analytics & compliance
│   │   ├── LivePobView.vue       # Live POB tracking
│   │   ├── WorkLocationView.vue  # Location management
│   │   ├── AssetsView.vue        # Asset management
│   │   ├── PermitPrintView.vue   # PTW print view
│   │   ├── LoginView.vue         # Login page
│   │   ├── ptw/
│   │   │   └── data-table.vue    # PTW data table component
│   │   └── work-location/
│   │       └── data-table.vue    # Work location data table
│   │
│   ├── layouts/                  # Layout components
│   │   └── DashboardLayout.vue   # Main dashboard layout with sidebar
│   │
│   ├── store/                    # State management
│   │   ├── theme.js              # Dark/Light mode theme store
│   │   ├── auth.js               # JWT authentication store
│   │   ├── vessel.js             # Vessel information store
│   │   └── websocket.js          # WebSocket connection store
│   │
│   ├── utils/                    # Utility functions
│   │   ├── csrf.js               # CSRF token handling (legacy)
│   │   ├── api.js                # API client with JWT auth
│   │   └── notifications.js      # Toast notification helpers
│   │
│   ├── lib/                      # Library utilities
│   │   └── utils.js              # General utility functions (cn, etc)
│   │
│   ├── router/                   # Vue Router configuration
│   │   └── index.js              # Route definitions with auth guards
│   │
│   ├── App.vue                   # Root component
│   ├── main.js                   # App entry point
│   └── style.css                 # Global styles (if exists)
│
├── public/                       # Public static files
├── .env                          # Environment variables
├── index.html                    # HTML entry point
├── vite.config.js                # Vite configuration
├── components.json               # Reka UI configuration
├── jsconfig.json                 # JavaScript configuration
├── package.json                  # Dependencies
├── DESIGN.md                     # Design documentation
└── README.md                     # This file
```

---

## 🎨 Theme System (Dark Mode)

### Implementation
The application uses a reactive theme store with CSS custom properties for seamless dark/light mode switching.

**Theme Store** (`src/store/theme.js`):
```javascript
import { reactive } from 'vue';

export const themeState = reactive({
    isDark: false
});

export const initializeTheme = () => {
    // Load from localStorage or detect system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    themeState.isDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
    applyTheme();
};

export const toggleTheme = () => {
    themeState.isDark = !themeState.isDark;
    localStorage.setItem('theme', themeState.isDark ? 'dark' : 'light');
    applyTheme();
};

const applyTheme = () => {
    if (themeState.isDark) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
};
```

**CSS Variables**:
- Light mode: `:root` selector
- Dark mode: `.dark` selector
- All colors defined as CSS custom properties in Tailwind config

**Usage in Components**:
```vue
<template>
  <div class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
    <h1 class="text-2xl font-bold">Content</h1>
  </div>
</template>
```

**Theme Toggle**: Available in DashboardLayout component (top-right corner)

---

## 🔐 Authentication System

### JWT Token Authentication
The application uses JWT (JSON Web Token) authentication with access and refresh tokens.

**Auth Store** (`src/store/auth.js`):
```javascript
import { reactive } from 'vue';

export const authState = reactive({
    isAuthenticated: false,
    user: null,
    accessToken: null,
    refreshToken: null
});

export const login = async (username, password) => {
    // Call backend login API
    // Store tokens in authState
    // Store refresh token in localStorage
};

export const logout = () => {
    // Clear tokens
    // Clear localStorage
    // Redirect to login
};

export const refreshAccessToken = async () => {
    // Use refresh token to get new access token
};
```

**Token Storage**:
- **Access Token**: Stored in memory (authState) - expires in 60 minutes
- **Refresh Token**: Stored in localStorage - expires in 7 days
- **User Info**: Stored in authState (emp_id, full_name, role, groups)

**Authentication Flow**:
1. User logs in with username/password
2. Backend returns access token + refresh token + user info
3. Frontend stores tokens and user info
4. All API requests include `Authorization: Bearer <access_token>` header
5. When access token expires (401), automatically refresh using refresh token
6. When refresh token expires, redirect to login

**Role-Based Access**:
- **Worker**: Basic dashboard, submit PTW, report incidents, check-in/out
- **Safety Officer**: Approve/reject PTW, investigate incidents, view analytics
- **Admin**: Full access including user management and system settings

---

## 🔌 State Management

### 1. Theme Store (`store/theme.js`)
**Purpose**: Manages dark/light mode state

**State**:
- `isDark`: Boolean indicating current theme

**Methods**:
- `initializeTheme()`: Load saved theme or detect system preference
- `toggleTheme()`: Switch between dark and light mode
- `applyTheme()`: Apply theme class to document

**Persistence**: localStorage (`theme` key)

---

### 2. Auth Store (`store/auth.js`)
**Purpose**: Manages user authentication and authorization

**State**:
- `isAuthenticated`: Boolean indicating login status
- `user`: User object (emp_id, full_name, role, groups)
- `accessToken`: JWT access token (short-lived)
- `refreshToken`: JWT refresh token (long-lived)

**Methods**:
- `login(username, password)`: Authenticate user
- `logout()`: Clear session and redirect to login
- `refreshAccessToken()`: Get new access token using refresh token
- `checkAuth()`: Verify if user is authenticated
- `hasRole(role)`: Check if user has specific role
- `hasPermission(permission)`: Check if user has specific permission

**Persistence**: 
- Refresh token in localStorage
- Access token in memory only (security)

---

### 3. Vessel Store (`store/vessel.js`)
**Purpose**: Manages vessel-specific information and configuration

**State**:
- `vesselName`: Current vessel name
- `vesselInfo`: Vessel details and configuration
- `operationalStatus`: Current operational status

**Methods**:
- `loadVesselInfo()`: Load vessel configuration
- `updateVesselStatus()`: Update operational status

**Use Case**: Multi-vessel deployments, vessel-specific settings

---

### 4. WebSocket Store (`store/websocket.js`)
**Purpose**: Manages real-time WebSocket connection

**State**:
- `ws`: WebSocket connection instance
- `isConnected`: Connection status
- `reconnectAttempts`: Number of reconnection attempts

**Methods**:
- `connect()`: Establish WebSocket connection
- `disconnect()`: Close WebSocket connection
- `send(data)`: Send data through WebSocket
- `on(event, callback)`: Register event listener
- `reconnect()`: Attempt to reconnect

**Events**:
- `pob_dashboard`: POB location updates
- `ptw_updates`: PTW status changes
- `incident_alerts`: New incident reports
- `system_status`: System status changes

**Auto-reconnection**: Automatically reconnects on connection loss with exponential backoff

---

## 🔗 API Integration

### Base URL
Configured via environment variable:
```env
VITE_API_BASE_URL=http://localhost:8989/api/v1
VITE_WS_URL=ws://localhost:8989/ws/pob/
```

### API Client (`src/utils/api.js`)
Centralized API client with JWT authentication:

```javascript
export const apiClient = {
    async request(endpoint, options = {}) {
        const token = authState.accessToken;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
            credentials: 'include'
        });
        
        if (response.status === 401) {
            // Token expired, try to refresh
            await refreshAccessToken();
            return this.request(endpoint, options);
        }
        
        return response.json();
    },
    
    get(endpoint) { return this.request(endpoint); },
    post(endpoint, data) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(data) }); },
    patch(endpoint, data) { return this.request(endpoint, { method: 'PATCH', body: JSON.stringify(data) }); },
    delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
};
```

### Example API Calls

**Login**:
```javascript
const response = await apiClient.post('/auth/login/', {
    username: 'worker',
    password: 'worker123'
});
```

**Create PTW**:
```javascript
const response = await apiClient.post('/hse/ptw/', {
    permit_type: 'HOT_WORK',
    deck_location: 'Engine Room',
    description: 'Welding work',
    emp_id: 'EMP001'
});
```

**Get Incidents**:
```javascript
const response = await apiClient.get('/hse/incidents/?status=OPEN');
```

**Update Incident**:
```javascript
const response = await apiClient.patch('/hse/incidents/1/', {
    status: 'INVESTIGATING',
    investigation_notes: 'Initial investigation started'
});
```

### Error Handling
```javascript
try {
    const data = await apiClient.get('/hse/incidents/');
    // Handle success
} catch (error) {
    if (error.status === 401) {
        // Unauthorized - redirect to login
    } else if (error.status === 403) {
        // Forbidden - show permission error
    } else if (error.status === 404) {
        // Not found
    } else {
        // Other errors
    }
}
```

---

## 🎨 UI Components

### Reka UI Components
Pre-built, accessible UI components from Reka UI:
- Button, Card, Dialog, Input, Label
- Select, Checkbox, Radio, Switch
- Table, Tabs, Toast, Tooltip
- ScrollArea, Separator, Badge
- Popover, Dropdown Menu, Context Menu

### Custom Components

**DashboardStats.vue**:
- Displays key metrics (Live Headcount, Active Permits, Days Without LTI, etc)
- Real-time updates via WebSocket
- Color-coded status indicators

**PobVisualMap.vue**:
- Interactive location map showing personnel distribution
- Real-time location updates
- Click to view personnel details

**IncidentReportForm.vue**:
- Multi-step incident reporting
- Severity level selection
- Proof image upload
- Location and employee information

**PtwModal.vue**:
- Complete PTW workflow modal
- Multi-step form (create, approve, start, mark done, close)
- Digital signature capture
- Rejection reason tracking

**Analytics Components** (`src/components/analytics/`):
- **SafetyMetricsTab.vue**: Daily safety metrics with charts
- **IncidentTrendsTab.vue**: Historical incident trends
- **ComplianceReportsTab.vue**: ISO 45001 compliance reports
- **LocationHotspotsTab.vue**: High-risk location identification
- **ConditionChangeAuditTab.vue**: System status change audit trail

---

## 📊 Analytics & Charts

### Chart.js Integration
Used for visualizing analytics data:
- **Line Charts**: Incident trends over time
- **Bar Charts**: Safety metrics comparison
- **Doughnut Charts**: Compliance score breakdown
- **Radar Charts**: Location risk assessment

### Theme-aware Charts
Charts automatically adapt to dark/light mode using computed colors:

```javascript
const chartColors = computed(() => ({
    primary: themeState.isDark ? '#3b82f6' : '#1e40af',
    danger: themeState.isDark ? '#ef4444' : '#dc2626',
    success: themeState.isDark ? '#10b981' : '#059669',
    warning: themeState.isDark ? '#f59e0b' : '#d97706'
}));
```

### Data Table Integration
TanStack Vue Table for complex data display:
- Sorting, filtering, pagination
- Column visibility toggle
- Row selection
- Responsive design

---

## 🚀 Development

### Available Scripts

```bash
# Start development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview
```

### Development Server
- Runs on `http://localhost:5173`
- Hot Module Replacement (HMR) enabled
- Auto-reload on file changes
- Proxy API requests to backend

### Code Style
- Vue 3 Composition API with `<script setup>`
- Reactive stores for state management
- Tailwind CSS for styling
- Reka UI for components
- ESLint for code linting (if configured)

### Debugging
```javascript
// Vue DevTools
// Install Vue DevTools browser extension for debugging

// Console logging
console.log('Debug info:', data);

// Network tab
// Check API requests and responses in browser DevTools

// WebSocket debugging
// Monitor WebSocket messages in browser DevTools
```

---

## 🏗️ Build & Deployment

### Production Build

```bash
# Build for production
npm run build

# Output directory: dist/
# Contains optimized, minified assets
```

### Environment Variables (Production)

```env
VITE_API_BASE_URL=https://api.example.com/api/v1
VITE_WS_URL=wss://api.example.com/ws/pob/
```

**Note**: Use `wss://` (WebSocket Secure) for HTTPS deployments

### Deployment Checklist
- [ ] Update `VITE_API_BASE_URL` to production API
- [ ] Update `VITE_WS_URL` to production WebSocket (wss://)
- [ ] Build with `npm run build`
- [ ] Test production build with `npm run preview`
- [ ] Deploy `dist/` folder to web server
- [ ] Configure CORS on backend for production domain
- [ ] Enable HTTPS/SSL with valid certificate
- [ ] Configure CDN for static assets (optional)
- [ ] Set up monitoring and error tracking
- [ ] Configure security headers (CSP, X-Frame-Options, etc)

### Nginx Configuration (Example)

```nginx
server {
    listen 443 ssl http2;
    server_name app.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    root /var/www/hse-frontend/dist;
    index index.html;
    
    # SPA routing - all requests go to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://backend:8989;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket proxy
    location /ws/ {
        proxy_pass http://backend:8989;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker Deployment (Example)

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🔐 Security

### Authentication Security
- JWT tokens with expiration
- Refresh token rotation
- Secure token storage (memory + localStorage)
- Automatic token refresh on expiration
- Logout clears all tokens

### XSS Protection
- Vue.js template escaping by default
- No `v-html` with user input
- Input validation on all forms
- Content Security Policy (CSP) headers

### CSRF Protection
- Backend CSRF token validation (if needed)
- SameSite cookie attribute
- Secure flag on cookies

### Data Security
- No sensitive data in localStorage (except theme preference)
- HTTPS/TLS for all communications
- Secure WebSocket (WSS) for production
- Input validation and sanitization

### Best Practices
- Keep dependencies updated
- Regular security audits
- Monitor for vulnerabilities
- Implement rate limiting on backend
- Use environment variables for secrets

---

## 🐛 Troubleshooting

### Issue: Dark mode not working
**Solution**:
- Clear browser cache and localStorage
- Verify theme store is initialized in `main.js`
- Check if `.dark` class is applied to `<html>` element
- Check browser console for errors

### Issue: API calls failing
**Solution**:
- Verify backend is running on correct port (8989)
- Check CORS configuration in backend settings
- Verify `VITE_API_BASE_URL` in `.env`
- Check browser console for error messages
- Verify JWT token is valid and not expired

### Issue: WebSocket not connecting
**Solution**:
- Ensure backend is using Daphne (not Django dev server)
- Verify WebSocket URL matches backend (`ws://` or `wss://`)
- Check browser console for connection errors
- Verify firewall allows WebSocket connections
- Check CORS settings for WebSocket

### Issue: Login not working
**Solution**:
- Verify backend seed users were created (`python manage.py seed_auth_users`)
- Check credentials are correct
- Verify backend is running and accessible
- Check browser console for API errors
- Clear localStorage and try again

### Issue: Real-time updates not showing
**Solution**:
- Verify WebSocket is connected (check browser DevTools)
- Check WebSocket store is properly initialized
- Verify backend is sending WebSocket events
- Check browser console for WebSocket errors
- Try refreshing the page

### Issue: Build fails
**Solution**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite

# Try building again
npm run build
```

---

## 📚 Resources

### Official Documentation
- **Vue 3**: https://vuejs.org/
- **Vite**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Reka UI**: https://reka-ui.com/
- **Chart.js**: https://www.chartjs.org/
- **Vue Router**: https://router.vuejs.org/
- **VueUse**: https://vueuse.org/

### Project Resources
- **Backend API**: http://localhost:8989/api/schema/swagger/
- **Design System**: See DESIGN.md
- **Git Repository**: Internal project repository

### Learning Resources
- Vue 3 Composition API Guide
- Tailwind CSS Documentation
- Chart.js Documentation
- WebSocket Best Practices

---

## 📝 Changelog

### Version 2.1.0 (May 29, 2026)
- ✅ Updated README with accurate project structure
- ✅ Fixed authentication method (JWT instead of session-based)
- ✅ Added vessel.js store documentation
- ✅ Added api.js and notifications.js utilities
- ✅ Updated UI library (Reka UI instead of Shadcn/Vue)
- ✅ Added AssetsView.vue documentation
- ✅ Improved deployment instructions with Docker example
- ✅ Added comprehensive troubleshooting section
- ✅ Added security best practices

### Version 2.0.0 (May 28, 2026)
- ✅ Vue 3 with Composition API
- ✅ Vite build tool
- ✅ Tailwind CSS v4
- ✅ Real-time WebSocket updates
- ✅ Dark mode support
- ✅ Role-based UI
- ✅ Analytics dashboard
- ✅ PTW workflow management

---

**Last Updated**: May 29, 2026  
**Version**: 2.1.0  
**Status**: Production Ready ✅  
**Node.js**: 18.0+  
**Vue**: 3.5+  
**Vite**: 8.0+

---

**Maintained by**: Saipem HSE Development Team
