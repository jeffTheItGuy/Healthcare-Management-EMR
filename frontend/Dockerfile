# syntax=docker/dockerfile:1

# ----------------------------------------------------------
# Stage 1: Install dependencies
# ----------------------------------------------------------
FROM node:20-slim AS deps
WORKDIR /app

COPY package.json ./
RUN npm install

# ----------------------------------------------------------
# Stage 2: Build Angular app
# ----------------------------------------------------------
FROM node:20-slim AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ----------------------------------------------------------
# Stage 3: Serve with nginx
# ----------------------------------------------------------
FROM nginx:alpine
COPY --from=builder /app/dist/zim-emr/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]