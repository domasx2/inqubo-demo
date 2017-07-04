FROM node:7
RUN git clone https://github.com/domasx2/inqubo-ui.git
WORKDIR inqubo-ui
RUN npm i
RUN npm run build
ENV NODE_ENV production
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh wait-for-it.sh
RUN chmod a+x wait-for-it.sh
CMD ./wait-for-it.sh rabbitmq:5672 -- node ./server.js
