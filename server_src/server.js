// import packages
require("dotenv").config();
const express = require('express')

// import the IP and port number
const hostname = process.env.HOSTNAME || '127.0.0.1';
const port = process.env.PORT || 9001;

// create the app
const app = express()

// use JSON module
app.use(express.json())

// import the routes
require('./config/routes')(app)

// import the api 
require('./config/api')(app)

// start the server
app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
