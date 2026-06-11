const express = require("express");
const app = express();
const password = "Admin123"
app.get("/", (req, res) => {
    const userInput = req.query.cmd;

    eval(userInput);

    res.send("Executed");
});

app.listen(3000);
