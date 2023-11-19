const fs = require('fs');
const csvParser = require("csv-parser");

const result = [];
fs.createReadStream("./queries.csv")
  .pipe(csvParser({
  }))
  .on("data", (data) => {
    console.log(data.url)
    result.push(data);
  })
  .on("end", () => {
    console.log("Done");
  });
