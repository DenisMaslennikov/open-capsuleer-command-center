/** Primitives and semantic aliases: the only source of visual decisions. */
export const primitives = {
  color: {
    gray050: "#f7f8fa",
    gray100: "#eef0f4",
    gray200: "#dde1e8",
    gray500: "#6b7280",
    gray900: "#1f2328",
    white: "#ffffff",
    indigo600: "#3b5bdb",
    indigo700: "#2f49b0",
    green600: "#2f9e44",
    red600: "#e03131",
    amber600: "#e8a13a",
  },
  space: { xxs: 4, xs: 8, sm: 12, md: 16, lg: 24, xl: 32, xxl: 48 },
  radius: { sm: 4, md: 8, lg: 12 },
  font: {
    family: "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif",
    size: { sm: 12, md: 14, lg: 16, xl: 20, xxl: 28 },
    weight: { regular: 400, medium: 500, bold: 600 },
  },
  motion: { fast: "120ms", base: "180ms" },
} as const;

export const tokens = {
  colorBgLayout: primitives.color.gray050,
  colorBgContainer: primitives.color.white,
  colorBorder: primitives.color.gray200,
  colorText: primitives.color.gray900,
  colorTextSecondary: primitives.color.gray500,
  colorPrimary: primitives.color.indigo600,
  colorPrimaryHover: primitives.color.indigo700,
  colorSuccess: primitives.color.green600,
  colorError: primitives.color.red600,
  colorWarning: primitives.color.amber600,

  spaceXxs: primitives.space.xxs,
  spaceXs: primitives.space.xs,
  spaceSm: primitives.space.sm,
  spaceMd: primitives.space.md,
  spaceLg: primitives.space.lg,
  spaceXl: primitives.space.xl,
  spaceXxl: primitives.space.xxl,

  radiusSm: primitives.radius.sm,
  radiusMd: primitives.radius.md,
  radiusLg: primitives.radius.lg,

  fontFamily: primitives.font.family,
  fontSizeSm: primitives.font.size.sm,
  fontSizeMd: primitives.font.size.md,
  fontSizeLg: primitives.font.size.lg,
  fontSizeXl: primitives.font.size.xl,
  fontSizeXxl: primitives.font.size.xxl,

  motionFast: primitives.motion.fast,
  motionBase: primitives.motion.base,
} as const;

export type Tokens = typeof tokens;
