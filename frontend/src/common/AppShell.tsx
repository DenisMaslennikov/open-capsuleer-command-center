import { Layout, Menu, Typography } from "antd";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { appRoutes } from "../app/routes";
import { LanguageSwitch } from "./LanguageSwitch";
import { tokens } from "../theme/tokens";

const { Header, Sider, Content, Footer } = Layout;

/** Common frame: top bar, page panel and the legal footer every page shares. */
export function AppShell() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const items = appRoutes.map((route) => ({
    key: route.path,
    icon: route.icon,
    label: t(route.labelKey),
  }));

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: tokens.colorBgContainer,
          borderBottom: `1px solid ${tokens.colorBorder}`,
          paddingInline: tokens.spaceLg,
        }}
      >
        <Typography.Title level={4} style={{ margin: 0 }}>
          {t("app.title")}
        </Typography.Title>
        <LanguageSwitch />
      </Header>
      <Layout>
        <Sider width={220} theme="light">
          <Menu
            mode="inline"
            selectedKeys={[pathname]}
            items={items}
            onClick={({ key }) => navigate(key)}
            style={{ borderInlineEnd: "none" }}
          />
        </Sider>
        <Content style={{ padding: tokens.spaceLg }}>
          <Outlet />
        </Content>
      </Layout>
      <Footer style={{ textAlign: "center", fontSize: 12, color: tokens.colorTextSecondary }}>
        {t("legal.ccpNotice")}
        <br />
        {t("legal.developerAgreement")}
      </Footer>
    </Layout>
  );
}
