var port = 'https://yushifamily.club';
var testPort = 'http://127.0.0.1:8001';
function getport(rl) {
    if(rl=='test'){
        return testPort;
    }else if(rl=='master'){
        return port;
    };
};

hostUrl = getport('master')
