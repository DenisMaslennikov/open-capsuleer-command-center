import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "./en.json";
import ru from "./ru.json";

const stored = globalThis.localStorage?.getItem("occc.locale");
const initial = stored === "ru" || stored === "en" ? stored : "en";

void i18n.use(initReactI18next).init({
  resources: { en: { translation: en }, ru: { translation: ru } },
  lng: initial,
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

i18n.on("languageChanged", (language) => {
  globalThis.localStorage?.setItem("occc.locale", language.startsWith("ru") ? "ru" : "en");
});

export default i18n;
