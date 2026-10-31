import createClient, { type Middleware } from "openapi-fetch";
import type { paths } from "./schema";

/** Access token kept in memory only; the refresh token lives in an HttpOnly cookie. */
let accessToken: string | null = null;

export function setAccessToken(token: string | null): void {
  accessToken = token;
}

const bearer: Middleware = {
  async onRequest({ request }) {
    if (accessToken) {
      request.headers.set("Authorization", `Bearer ${accessToken}`);
    }
    return request;
  },
};

export const api = createClient<paths>({
  baseUrl: "",
  credentials: "same-origin",
});
api.use(bearer);
