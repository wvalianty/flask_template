function get_parameters(){
    var urlParameters = location.search;
    var requestParametersMap = new Object();
    if (urlParameters.indexOf('?') != -1)
    {
        var parameters = decodeURI(urlParameters.substr(1));
        parameterArray = parameters.split('&');
        for (var i = 0; i < parameterArray.length; i++) {
            requestParametersMap[parameterArray[i].split('=')[0]] = (parameterArray[i].split('=')[1]);
        }
        return requestParametersMap;
    }
    else
    {
        return {}
    }
}

// function get_url(parameters_map, parameter_names) {
//     for( var key in parameters_map) {
//         if (! parameters_map.hasOwnProperty(key)){
//             return false;
//         }
//     }
//
//     url = location.protocol + "//" + location.hostname + ":" + location.port + location.pathname ;
//     url = url + "?";
//
//     for (var i = 0; i < parameter_names.length; i++){
//            url = url + parameter_names[i] + parameters_map[parameter_names[i]];
//            if( i < parameter_names.length -1 ) {
//                 url = url + "&";
//            }
//     }
//
//     return url;
// }