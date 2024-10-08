# FRONTEND
FROM node:16 AS build

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

RUN chown -R node:node /app/node_modules

RUN npm run build


CMD ["npm", "run", "dev"]
