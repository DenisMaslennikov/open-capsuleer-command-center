import { DashboardOutlined } from "@ant-design/icons";
import type { ReactNode } from "react";
import { DashboardPage } from "../pages/dashboard/DashboardPage";

export type AppRoute = {
  path: string;
  labelKey: string;
  icon: ReactNode;
  element: ReactNode;
};

/** Single registry: the side panel and the router are built from the same list. */
export const appRoutes: AppRoute[] = [
  { path: "/", labelKey: "nav.dashboard", icon: <DashboardOutlined />, element: <DashboardPage /> },
];
