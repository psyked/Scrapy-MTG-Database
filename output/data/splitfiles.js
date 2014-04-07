var fs = require("fs");
var fileData = (JSON.parse(fs.readFileSync("./items.json", "utf8")));
var outputData = {};
for (var i = 0, l = fileData.length; i < l; i++) {
    var item = fileData[i];
    for (var j = 0, k = item.allsets.length; j < k; j++) {
        var key = item.allsets[j].toLowerCase();
        key = key.replace(/\(([^()]+)\)/g, '');
        key = key.replace(/(?:(?:^|\n)\s+|\s+(?:$|\n))/g, '');
        key = key.replace(/[\s|\:|\.]/g, '-');
        if (!outputData[key]) {
            outputData[key] = [];
        }
        outputData[key].push(item);
    }
}

for (var expansion in outputData) {
    var outputString = JSON.stringify(outputData[expansion], null, 4);
    var outputFilename = './' + expansion + '.json';

    fs.writeFile(outputFilename, outputString, function (err) {
        if (err) {
            console.log(err);
        } else {
            console.log("JSON saved to " + outputFilename);
        }
    });
}