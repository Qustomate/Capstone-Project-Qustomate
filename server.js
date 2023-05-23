const express = require("express");
const app = express();
const port =  8080;
const router = require("./routes/routes");

//menggunakan router
app.use(router);


  app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })