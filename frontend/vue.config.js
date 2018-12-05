module.exports = {
    assetsDir: 'static/admin/',
    runtimeCompiler: true,
    productionSourceMap: false,
    devServer: {
        port: process.env.PORT || 8080,
        host: 'localhost',
        https: false, // https:{type:Boolean}
        open: true, //配置自动启动浏览器
        proxy: {
            '/api/': {
                target: 'http://127.0.0.1:8001/',
                changeOrigin: true,
            },
            '/static/': {
                target: 'http://127.0.0.1:8001/',
                changeOrigin: true,
            }
        }
    }
}