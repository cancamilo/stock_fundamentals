FROM node:18-alpine

WORKDIR /app

COPY ./frontend/package.json ./

RUN npm install

RUN npm i -g serve

COPY ./frontend .

RUN npm run build

EXPOSE 8080

CMD [ "serve", "-s", "dist", "-p", "8080"]
