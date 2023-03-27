const { exec } = require("child_process");
const fs = require('fs');

module.exports = function (app) {
    app.route('/run_example').get(runExample)    
}

function runExample(req, res) {
 
  exec("python3 ../core/extract.py --src ../cps.owl --des ../truncated.owl", (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
    }
    if (stderr) {
        console.log(`stderr: ${stderr}`);
    }

    // attempt to read from file
   
        
    // return the file
    console.log(`stdout: ${stdout}`);
    res.set('Content-Type', 'text/html');
    res.download("../truncated.owl");
  });
}