FROM node:14.8.0-alpine3.12

WORKDIR .

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]
COPY . ./

ENV FRONTEND_PERSON_URL="http://localhost:30001/api/persons"
ENV REACT_APP_FRONTEND_LOCATION_URL="http://localhost:30002/api/locations"


EXPOSE 3000

CMD ["npm", "start"]

