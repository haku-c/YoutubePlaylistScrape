var fs = require('fs');

var data = fs.readFileSync('queries.csv')
  .toString() // convert Buffer to string
  .split('\n') // split string to lines
  .map(e => e.trim()) // remove white spaces for each line
  .map(e => e.split(',').map(e => e.trim())); // split each line to array

console.log(data);
console.log(JSON.stringify(data, '', 2));