Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

var sorter = function(a, b) {
     return a[0] - b[0];
};

function toArray(obj) {
    var result = [];
    for (var prop in obj) {
        var value = obj[prop];
        if (typeof value === 'object') {
            result.push(toArray(value)); // <- recursive call
        } else {
            var time = parseInt(prop,10);
            result.push([time,value]);
        }
    }
    return result;
}
