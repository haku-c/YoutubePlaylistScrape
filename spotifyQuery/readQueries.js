const fs = require('fs');
const csvParser = require("csv-parser");

var result = [];
fs.createReadStream("./queries.csv")
  .pipe(csvParser())
  .on("data", (data) => {
    result.push(data);
  })
  .on("end", () => {
    console.log(result[0]);
  });