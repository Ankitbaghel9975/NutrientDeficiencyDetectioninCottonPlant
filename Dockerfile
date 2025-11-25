FROM node:20-alpine
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 5173
# dev command provided by compose (npm run dev -- --host)
