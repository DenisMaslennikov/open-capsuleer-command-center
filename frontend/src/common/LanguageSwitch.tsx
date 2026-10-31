import { Segmented } from "antd";
import { useTranslation } from "react-i18next";

const LOCALES = ["en", "ru"] as const;

export function LanguageSwitch() {
  const { i18n } = useTranslation();
  const current = i18n.language.startsWith("ru") ? "ru" : "en";

  return (
    <Segmented
      size="small"
      value={current}
      options={LOCALES.map((locale) => ({ label: locale.toUpperCase(), value: locale }))}
      onChange={(value) => void i18n.changeLanguage(value)}
    />
  );
}
