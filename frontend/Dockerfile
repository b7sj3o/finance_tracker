# Вказуємо базовий образ
FROM node:16 AS build

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо package.json та package-lock.json
COPY package*.json ./

# Встановлюємо залежності
RUN npm install

# Копіюємо весь код
COPY . .

# Будуємо проект
RUN npm run build

# Вказуємо образ для веб-сервера
# FROM node:16

# # Встановлюємо робочу директорію
# WORKDIR /usr/src/app

# # Копіюємо зібраний додаток
# COPY --from=build /app/dist /usr/src/app


# # Виставляємо порт
# EXPOSE 3000

# # Запускаємо додаток
CMD ["npm", "start"]
