import { createRouter, createWebHistory } from 'vue-router';
import { checkAuth, authState } from '@/store/auth';

const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: () => import('@/views/AdminDashboardView.vue'),
        meta: { requiresAuth: true, requiredRole: 'Admin' }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/LoginView.vue'),
        meta: { requiresGuest: true }
    },
    // HSE Module Routes
    {
        path: '/hse',
        name: 'HSEDashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/hse/live-pob',
        name: 'LivePob',
        component: () => import('@/views/LivePobView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/hse/ptw',
        name: 'Ptw',
        component: () => import('@/views/PtwView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/hse/incidents',
        name: 'Incidents',
        component: () => import('@/views/IncidentsView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/offshore/locations',
        name: 'WorkLocation',
        component: () => import('@/views/WorkLocationView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/hse/analytics',
        name: 'Analytics',
        component: () => import('@/views/AnalyticsView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    {
        path: '/hse/permit-print/:id',
        name: 'PermitPrint',
        component: () => import('@/views/PermitPrintView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hse' }
    },
    // HR Module Routes
    {
        path: '/hr',
        name: 'HRDashboard',
        component: () => import('@/views/hr/HRDashboardView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hr' }
    },
    {
        path: '/hr/personnel',
        name: 'HRPersonnel',
        component: () => import('@/views/hr/PersonnelView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hr' }
    },
    {
        path: '/hr/roster',
        name: 'HRRoster',
        component: () => import('@/views/hr/RosterView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hr' }
    },
    {
        path: '/hr/payroll',
        name: 'HRPayroll',
        component: () => import('@/views/hr/PayrollView.vue'),
        meta: { requiresAuth: true, requiredModule: 'hr' }
    },
    // Offshore Routes
    {
        path: '/offshore/vessels',
        name: 'VesselRegistry',
        component: () => import('@/views/admin/VesselRegistryView.vue'),
        meta: { requiresAuth: true, requiredRole: 'Admin' }
    },
    {
        path: '/admin/users',
        name: 'UserManagement',
        component: () => import('@/views/admin/UserManagementView.vue'),
        meta: { requiresAuth: true, requiredRole: 'Admin' }
    },
    // Asset Module Routes
    {
        path: '/assets/dashboard',
        name: 'AssetsDashboard',
        component: () => import('@/views/AssetsDashboardView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    },
    {
        path: '/assets',
        name: 'Assets',
        component: () => import('@/views/AssetsView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    },
    {
        path: '/assets/work-orders',
        name: 'WorkOrders',
        component: () => import('@/views/WorkOrdersView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    },
    {
        path: '/assets/machinery',
        name: 'Machinery',
        component: () => import('@/views/MachineryView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    },
    {
        path: '/assets/inventory',
        name: 'Inventory',
        component: () => import('@/views/InventoryView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    },
    {
        path: '/assets/spareparts',
        name: 'Spareparts',
        component: () => import('@/views/SparepartsView.vue'),
        meta: { requiresAuth: true, requiredModule: 'asset' }
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

function getDefaultRoute() {
    if (!authState.isLoggedIn) {
        return '/login';
    }
    if (authState.userRole === 'Admin') {
        return '/';
    }
    if (authState.accessibleModules && authState.accessibleModules.includes('hr')) {
        return '/hr';
    }
    if (authState.accessibleModules && authState.accessibleModules.includes('asset')) {
        return '/assets/dashboard';
    }
    if (authState.accessibleModules && authState.accessibleModules.includes('hse')) {
        return '/hse';
    }
    return '/login';
}

router.beforeEach(async (to, from, next) => {
    // If auth state is not checked yet (e.g. initial load), check it
    if (authState.isAuthChecking) {
        await checkAuth();
    }

    const isAuthenticated = authState.isLoggedIn;

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    } else if (to.meta.requiresGuest && isAuthenticated) {
        // Redirect authenticated users to their home page based on role/modules
        next(getDefaultRoute());
    } else if (to.meta.requiredModule) {
        // Check if user has access to the required module
        const hasAccess = authState.accessibleModules &&
                         authState.accessibleModules.includes(to.meta.requiredModule);
        if (!hasAccess) {
            next(getDefaultRoute());
        } else {
            next();
        }
    } else if (to.meta.requiredRole) {
        // Check if user has the required role
        if (authState.userRole !== to.meta.requiredRole) {
            next(getDefaultRoute());
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
