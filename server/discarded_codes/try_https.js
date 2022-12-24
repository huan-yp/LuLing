import http from "http"
import https from "https"
import request from "request"

const PROXY_HOST = "localhost"
const PROXY_PORT = 7890


function getURL(url) {
    request({
        url: url,
        proxy: "http://localhost:7890", 
        headers: {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "CookieConsent=true; _ga=GA1.2.297726615.1671708376; _gid=GA1.2.1162552331.1671708376; sessionid=l28r9txpkthbai6t5ei3zcfbl9uj1gil; __cf_bm=KF8uvTuMoGarFIVGkpBf.3pcN3nJnz0mSAzVWTbapLc-1671710089-0-AUMUhAz5DB9esEpwweuOqYzKIchnQP7ZLjs7fzSQgL891RnOxm+HMHABgVzWmZkIpbGI8tGF5VQyKOjAG3go/oGImSjILJbEDO5n23WSdRbOJRemgZsxw/H30gMuoA7MGgipk/oOqDITxjIyNI09utRC5Xyz2WIKmVMW78luM5hDbMQ0MHOB6bX13rIclfUkcQ==; csrftoken=nCAmR3JmaABuT8aJwQIfg3HMHMNGxmpC",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        }
    }, function (error, response, body) {
        if (error) {
            // console.log(response.statusCode)
            console.log(error);
        } else {
            // console.log(response.request)
            console.log(response.statusCode)
            console.log(response.headers)
            // console.log(body);
        }
    });


}

const url = "http://beta.character.ai/"
// const url = "https://www.google.com/"
getURL(url)
