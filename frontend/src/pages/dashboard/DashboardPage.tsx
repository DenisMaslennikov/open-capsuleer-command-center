import { Alert, Card, Descriptions, Space, Typography } from "antd";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { api } from "../../api/client";
import { tokens } from "../../theme/tokens";

type Meta = {
  env: string;
  esi_configured: boolean;
  all_capabilities: string[];
};

export function DashboardPage() {
  const { t } = useTranslation();
  const meta = useQuery({
    queryKey: ["meta"],
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/meta");
      if (error) throw error;
      return data as unknown as Meta;
    },
  });

  return (
    <Space direction="vertical" size={tokens.spaceLg} style={{ width: "100%" }}>
      <header>
        <Typography.Title level={2} style={{ marginBottom: tokens.spaceXs }}>
          {t("dashboard.title")}
        </Typography.Title>
        <Typography.Text type="secondary">{t("dashboard.subtitle")}</Typography.Text>
      </header>

      {meta.isError && <Alert type="error" showIcon message={t("dashboard.error")} />}

      <Card title={t("dashboard.status")} loading={meta.isLoading}>
        {meta.data && (
          <Descriptions column={1} size="small">
            <Descriptions.Item label={t("dashboard.env")}>{meta.data.env}</Descriptions.Item>
            <Descriptions.Item label={t("dashboard.esi")}>
              {meta.data.esi_configured
                ? t("dashboard.configured")
                : t("dashboard.notConfigured")}
            </Descriptions.Item>
            <Descriptions.Item label={t("dashboard.capabilities")}>
              {meta.data.all_capabilities.join(", ")}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Card>
    </Space>
  );
}
