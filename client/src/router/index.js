import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login";
import Signup from "@/views/Auth/Signup";
import Home from "@/views/Home";
import Services from "@/views/services/Services";
import AddService from "@/views/services/AddService";
import Customers from "@/views/customers/Customers";
import AddCustomer from "@/views/customers/AddCustomer";
import Customer from "@/views/customers/Customer";
import UpdateCustomer from "@/views/customers/UpdateCustomer";
import store from "@/store";

const routes = [
  {
    path: "/:catchAll(.*)", // reroute undefined paths
    redirect: "/dashboard/customers",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  // {
  //   path: "/signup",
  //   name: "Signup",
  //   component: Signup,
  // },
  {
    path: "/dashboard/services",
    name: "Services",
    component: Services,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/add-service",
    name: "AddService",
    component: AddService,
    meta: {
      requireLogin: true,
      requireAdmin: true,
    },
  },
  {
    path: "/dashboard/customers",
    name: "Customers",
    component: Customers,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/add-customer",
    name: "AddCustomer",
    component: AddCustomer,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/customers/:id",
    name: "Customer",
    component: Customer,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/dashboard/updateCustomers/:id",
    name: "UpdateCustomer",
    component: UpdateCustomer,
    meta: {
      requireLogin: true,
    },
  },

  // {
  //   path: "/about",
  //   name: "about",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  // },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (
    to.matched.some((m) => m.meta.requireLogin) &&
    !store.state.isAuthenticated
  ) {
    next({ name: "Login" });
  } else if (
    to.matched.some((m) => m.meta.requireAdmin) &&
    !store.state.user.is_staff
  ) {
    next({ name: "Customers" });
  } else next();
});
export default router;
