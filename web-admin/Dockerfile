# build stage
FROM node:alpine as build-stage
WORKDIR /app
COPY package.json ./
RUN yarn install 
COPY . .
RUN yarn run build


# production stage
FROM nginx:stable-alpine
COPY --from=build-stage /app/build /usr/share/nginx/html
COPY --from=build-stage /app/nginx/nginx.template /etc/nginx/conf.d/nginx.template
EXPOSE 80
CMD ["/bin/sh", "-c", "exec nginx -g 'daemon off;'"]
