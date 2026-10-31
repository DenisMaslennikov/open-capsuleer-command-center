import type { ThemeConfig } from "antd";
import { tokens } from "./tokens";

/** Ant Design theme derived from the semantic tokens; nothing else may configure it. */
export const antdTheme: ThemeConfig = {
  token: {
    colorPrimary: tokens.colorPrimary,
    colorSuccess: tokens.colorSuccess,
    colorError: tokens.colorError,
    colorWarning: tokens.colorWarning,
    colorText: tokens.colorText,
    colorTextSecondary: tokens.colorTextSecondary,
    colorBorder: tokens.colorBorder,
    colorBgLayout: tokens.colorBgLayout,
    colorBgContainer: tokens.colorBgContainer,
    borderRadius: tokens.radiusMd,
    fontFamily: tokens.fontFamily,
    fontSize: tokens.fontSizeMd,
    motionDurationFast: tokens.motionFast,
    motionDurationMid: tokens.motionBase,
    padding: tokens.spaceMd,
    paddingLG: tokens.spaceLg,
  },
  components: {
    Layout: {
      headerBg: tokens.colorBgContainer,
      bodyBg: tokens.colorBgLayout,
      siderBg: tokens.colorBgContainer,
      footerBg: tokens.colorBgLayout,
    },
    Menu: {
      itemSelectedBg: tokens.colorBgLayout,
      itemSelectedColor: tokens.colorPrimary,
    },
  },
};
