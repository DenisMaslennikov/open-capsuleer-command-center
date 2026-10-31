import { describe, expect, it } from "vitest";
import { antdTheme } from "./antd";
import { primitives, tokens } from "./tokens";

describe("design tokens", () => {
  it("maps every semantic colour onto a primitive colour", () => {
    const palette = new Set<string>(Object.values(primitives.color));
    const semantic = Object.entries(tokens).filter(([key]) => key.startsWith("color"));

    expect(semantic.length).toBeGreaterThan(0);
    for (const [, value] of semantic) {
      expect(palette.has(String(value))).toBe(true);
    }
  });

  it("derives the component library theme from the tokens", () => {
    expect(antdTheme.token?.colorPrimary).toBe(tokens.colorPrimary);
    expect(antdTheme.token?.borderRadius).toBe(tokens.radiusMd);
    expect(antdTheme.token?.fontFamily).toBe(tokens.fontFamily);
  });
});
