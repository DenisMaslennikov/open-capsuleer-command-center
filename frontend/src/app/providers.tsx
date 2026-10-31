import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider } from "antd";
import enUS from "antd/locale/en_US";
import ruRU from "antd/locale/ru_RU";
import { useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { antdTheme } from "../theme/antd";

export function AppProviders({ children }: { children: ReactNode }) {
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: { retry: 1, refetchOnWindowFocus: false, staleTime: 30_000 },
        },
      }),
  );
  const { i18n } = useTranslation();

  return (
    <QueryClientProvider client={client}>
      <ConfigProvider theme={antdTheme} locale={i18n.language.startsWith("ru") ? ruRU : enUS}>
        {children}
      </ConfigProvider>
    </QueryClientProvider>
  );
}
