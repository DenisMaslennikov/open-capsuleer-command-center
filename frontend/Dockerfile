FROM node:26-alpine AS base

ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""
ARG NO_PROXY=""
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

FROM base AS dev
CMD ["npm", "run", "dev"]

FROM base AS build
RUN npm run build

FROM nginx:1.29-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
