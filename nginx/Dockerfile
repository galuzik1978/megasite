FROM node:latest as ui-builder

# делаем каталог 'app' текущим рабочим каталогом
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# копируем оба 'package.json' и 'package-lock.json' (если есть)
COPY frontend/package*.json ./
# COPY package.json /usr/src/package.json


# устанавливаем зависимости проекта
RUN npm install
COPY ./frontend .
RUN npm run build

# start app
FROM nginx as production-stage
RUN mkdir /usr/src/app
COPY  --from=ui-builder /usr/src/app/dist /usr/src/app
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
COPY nginx/nginx.conf /etc/nginx/nginx.conf