FROM node:16.10.0-alpine3.11

RUN mkdir -p /opt/app
RUN apk update && apk add bash
RUN apk add --no-cache libc6-compat

ENV PORT 3000

WORKDIR /opt/app

COPY package.json package-lock.json /opt/app/

RUN npm install

COPY ./ /opt/app
