# Вказуємо базовий образ
FROM node:16 AS build

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо package.json та package-lock.json
COPY package*.json .

# Встановлюємо залежності
RUN npm install

# Копіюємо весь код
COPY . .

RUN chown -R node:node /app/node_modules

# Будуємо проект
RUN npm run build


# # Запускаємо додаток
CMD ["npm", "run", "dev"]
