const { exec } = require("child_process");
const fs = require('fs');
const tmp = require('tmp');

module.exports = function (app) {
    app.route('/run_example').get(runExample);    
    app.route('/extract').post(extractRequestHandler);
}

function runExample(req, res) {

    const desSrc = tmp.fileSync();
    desPath = desSrc.name

    exec(`python3 ../core/extract.py --src ../cps.owl --des "${desPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            res.error("An error occured while parsing the data");
            desSrc.removeCallback();
            return;
        }  // end if
        
        if (stderr) {
            console.log(`stderr: ${stderr}`);
        } // end if

        // return the file
        console.log(`stdout: ${stdout}`);
        res.download("../truncated.owl", filename="truncated.owl", (err) => {
            if (err)
                console.log("error: " + error);
            else 
                console.log("file removed");
            
            // unlink the temporary file
            desSrc.removeCallback();
        }); // end res.download
    });
    
} // end runExample

function extractRequestHandler(req, res) {

} // end extractRequestHandler
