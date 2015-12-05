var success = function(data, status) {
    $("#form").remove();
    var t = data.indexOf('<');
    var str = data;
    if ( t > -1 ) {
        $("#result")[0].textContent = data.substr(0, t);
        $("#result2")[0].innerHTML = data.substr(t);
    } else {
        $("#result")[0].innerHTML= data;
    }
};

