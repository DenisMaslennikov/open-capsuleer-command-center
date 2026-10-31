import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AppShell } from "../common/AppShell";
import { appRoutes } from "./routes";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: appRoutes.map((route) => ({ index: route.path === "/", path: route.path === "/" ? undefined : route.path, element: route.element })),
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
