import http from "http"
import https from "https"

const PROXY_HOST = "localhost"
const PROXY_PORT = 7890


function getURL(url, headers) {
    return new Promise((resolve, reject) => {
        const urlParsed = new URL(url);
        // headers = headers || {};
        // headers['Proxy-Authorization'] = 'Basic ' + Buffer.from(conf.proxy_username + ':' + conf.proxy_password).toString('base64');
        http.request({
            host: PROXY_HOST,
            port: PROXY_PORT,
            method: 'CONNECT',
            path: urlParsed.hostname,
            headers: headers,
            timeout: 60000,
        }).on('connect', (res, socket) => {
            if (res.statusCode === 200) {
                const agent = new https.Agent(socket);
                var req = https.get({
                    host: urlParsed.hostname,
                    path: urlParsed.pathname,
                    agent: agent,
                    headers: headers,
                    rejectUnauthorized: false
                }, (response) => {
                    const chunks = [];
                    response.on('data', (chunk) => {
                        chunks.push(chunk);
                    });
                    response.on('end', () => {
                        resolve({
                            body: Buffer.concat(chunks).toString(),
                            headers: response.headers,
                            status: response.statusCode
                        })
                    });

                    response.on("error", (err) => {
                        console.log("Get Error")
                        reject(err);
                    })

                    response.setTimeout(15000, () => {
                        reject('Timeout')
                    })
                });

                req.on('error', (err) => {
                    reject(err.message);
                })
            } else {
                reject('Could not connect to proxy!')
            }

        }).on('error', (err) => {
            reject(err.message);
        }).end();
    })

}

var headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}
// const url = "https://beta.character.ai/"
const url = "https://www.google.com/"
getURL(
    url, headers
).then(function (response) {
    console.log(response.headers)
    // console.log(response.body)
}).catch(function (error){
    console.log(error)
})