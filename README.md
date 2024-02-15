# Xrate
1. Download the `Dockerfile` and create the `users.yaml` file. Please remember these two files must be in the same directory.</br></br>
2. Build the docker image
   ```docker build  --build-arg timezone=<timezone> --tag <name>:<version> .```</br>
   E.g. ```docker build  --build-arg timezone=Europe/London --tag xrate:v1 .```</br></br>
3. Create a docker network. If you have a docker network configured for the desired subnet you can use that.</br>
   ```docker network create -d bridge <network-name> --subnet <your-subnet>```</br>
   E.g. ```docker network create -d bridge xrate-network --subnet 192.168.0.0/24```</br></br>
4. Run the container</br>
   ```docker run --name <container-name> -p <host-port>:5000 --network <docker-network> -d -t <name>:<version>```</br>
   E.g. ```docker run --name xrate -p 3000:5000 --network xrate-network -d -t xrate:v1```
## Create API users
   See the users.yaml file. Please use base64 encoded passwords.
## Request type
   Add this Header</br>
   `Content-Type`: `application/json`</br></br>
   Add `username` and `password` in the Body</br>
   \{
   "username": \<username\>,</br>
   "password": \<plain-text-password\></br>
   \}
## API reference
Endpoint: `/api/test/`, method: `GET`, does not require username and password.</br></br>
All API endpoints below require the username and password.</br></br>
Endpoint: `/api/convert/<from-currency>-<to-currency>/`, method: `GET`</br></br>
Endpoint: `/api/convert-all/<from-currency>/`, method: `GET`</br></br>
Endpoint: `/api/rates/update/`, method: `POST`</br></br>
Endpoint: `/api/<currency>/last-updated/`, method: `GET`</br></br>
