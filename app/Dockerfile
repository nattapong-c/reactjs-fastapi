FROM node:16-alpine as build-step
WORKDIR /app

COPY ./app/package.json ./app/yarn.lock ./
COPY ./app/src ./src
COPY ./app/public ./public
RUN yarn install
RUN yarn build

FROM nginx:stable-alpine
COPY --from=build-step ./app/build /usr/share/nginx/html
COPY ./app/nginx/nginx.default.conf /etc/nginx/conf.d/default.conf