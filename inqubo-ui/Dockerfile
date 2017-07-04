FROM node:7
RUN apt-get update && apt-get install -y curl apt-transport-https && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn
RUN git clone https://github.com/domasx2/inqubo-ui.git
WORKDIR inqubo-ui
RUN yarn install
RUN npm run build
ENV NODE_ENV production
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh wait-for-it.sh
RUN chmod a+x wait-for-it.sh
CMD ./wait-for-it.sh rabbitmq:5672 -- node ./server.js
