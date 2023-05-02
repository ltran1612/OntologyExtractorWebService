const { exec } = require("child_process");
const fs = require('fs');
const fsp = fs.promises;
const tmp = require('tmp');

module.exports = function (app) {
    app.route('/run_example').get(runExample);    
    app.route('/extract').post(extractRequestHandler);
}

function runExample(req, res) {

    const desSrc = tmp.fileSync();
    desPath = desSrc.name

    param_str = "Aspect Trustworthiness Human"

    exec(`python3 ../core/extract.py --src ../cps.owl --des "${desPath}" --list ${param_str}`, (error, stdout, stderr) => {
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

async function extractRequestHandler(req, res) {
    const desSrc = tmp.fileSync();
	const tmpFile = tmp.fileSync();
    desPath = desSrc.name
	tmpPath = tmpFile.name

	console.log(req.body);
	body = req.body;
    base_command = `python3 ../core/extract.py --src ../cps.owl --des "${desPath}"` 

    // loop through the classes
	param_str = ""
	let use_sparlq = true
    for (let myclass of Object.keys(body)) {
		console.log(myclass);
		if (myclass === "sparql") {
			sparql_query = body[myclass];
			const writePromise = await fsp.writeFile(tmpPath, sparql_query);
		} else {
			use_sparlq = false
    		class_with_instances = req.body;
    		param_str = ""
			temp = class_with_instances[myclass];
			// add the class
			temp.unshift(myclass);
			// convert to string
			param_str = temp.join(" ");
			// add the ending
			param_str += " -";
		} // end else
    } // end for
	
	if (use_sparlq) {
		command = base_command + " " + `--sparql ${tmpPath}`
	}
	else {
		command = base_command + " " + `--list ${param_str}`
	} // end else

   	console.log(command)
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            res.send("An error occured while parsing the data");
            desSrc.removeCallback();
			tmpFile.removeCallback();
            return;
        }  // end if
        
        if (stderr) {
            console.log(`stderr: ${stderr}`);
        } // end if

        // return the file
        console.log(`stdout: ${stdout}`);
        res.download(desPath, filename="truncated.owl", (err) => {
            if (err)
                console.log("error: " + error);
            else 
                console.log("file removed");
            
            // unlink the temporary file
            desSrc.removeCallback();
			tmpFile.removeCallback();
        }); // end res.download
    });
} // end extractRequestHandler
