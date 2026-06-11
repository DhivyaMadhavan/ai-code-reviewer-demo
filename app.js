const express = require("express");
const app = express();
const PASSWORD = "admin"
app.get("/", (req, res) => {
    const userInput = req.query.cmd;

    eval(userInput);

    res.send("Executed");
});

app.listen(3000);
