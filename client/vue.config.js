module.exports = {
  publicPath: 'http://127.0.0.1:8080',
  outputDir: '../static/dist',
  indexPath: '../../templates/base-vue.html',

  chainWebpack: config => {
    config.devServer.writeToDisk(true);
  }
}