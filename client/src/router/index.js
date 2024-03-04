import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";

const routes = [
  {
    path: "/:catchAll(.*)", // reroute undefined paths to dashboard
    redirect: "/dashboard",
  },
  {
    path: "/login", //LOGIN PATH
    name: "Login",
    component: () =>
      import(/* webpackChunkName: "login" */ "@/views/Auth/Login"),
  },
  {
    path: "/dashboard", // DASHBOARD PATH
    name: "Dashboard",
    component: () =>
      import(/* webpackChunkName: "dashboard" */ "@/views/Dashboard"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/services", // DISPLAY SERVICES PATH
    name: "Services",
    component: () =>
      import(/* webpackChunkName: "services" */ "@/views/services/Services"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/add-service", // ADD A SERVICE PATH
    name: "AddService",
    component: () =>
      import(
        /* webpackChunkName: "add-service" */ "@/views/services/AddService"
      ),
    meta: {
      requireLogin: true,
      requireAdmin: true,
    },
  },
  {
    path: "/dashboard/customers", // DISPLAY CUSTOMERS PATH
    name: "Customers",
    component: () =>
      import(/* webpackChunkName: "customers" */ "@/views/customers/Customers"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/add-customer", // ADD A CUSTOMER PATH
    name: "AddCustomer",
    component: () =>
      import(
        /* webpackChunkName: "add-customer" */ "@/views/customers/AddCustomer"
      ),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/customers/:id", // SHOW CUSTOMER PROFILE PATH
    name: "Customer",
    component: () =>
      import(/* webpackChunkName: "customer" */ "@/views/customers/Customer"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/updateCustomers/:id", // UPDATE CUSTOMER PATH
    name: "UpdateCustomer",
    component: () =>
      import(
        /* webpackChunkName: "update-customer" */ "@/views/customers/UpdateCustomer"
      ),
    meta: {
      requireLogin: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const { isAuthenticated, user } = store.state;
  const requiresLogin = to.matched.some((route) => route.meta.requireLogin);
  const requiresAdmin = to.matched.some((route) => route.meta.requireAdmin);

  if (requiresLogin && !isAuthenticated) {
    //If employee is unauthenticated redirect to login page
    next({ name: "Login" });
  } else if (requiresAdmin && !user.is_staff) {
    // If auth employee tried to enter a page only ment for admins then he is redirected to dashboard
    next({ name: "Dashboard" });
  } else {
    next();
  }
});
export default router;
