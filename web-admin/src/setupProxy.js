const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = (app) => {
  app.use(
    createProxyMiddleware("/api", {
      target: "https://wxapi.rp-i.net",
      secure: false,
      pathRewrite: {
        "^/api": "",
      },
    })
  );
};
