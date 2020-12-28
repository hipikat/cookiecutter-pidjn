const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');
const path = require('path');

const ASSET_PATH = process.env.ASSET_PATH || 'var/build-webpack',
  STATIC_PATH = process.env.STATIC_PATH || '/static',
  PROJECT_PATH = path.join(__dirname, '..'),
  dev_debug_port = 9000,
  dev_prod_port  = 9001;
  

module.exports = env => {

  // Default to production
  if (!env) {
    env = { debug: false };
  }

  // Use e.g. `webpack --env (debug|prod)[,[no]minify][,(clean|dirty)]`,
  // or everything will just default to clean, minified production mode.
  //
  // - `debug` defaults to `nominify` and `dirty`
  // - `prod` defaults to `minify` and `clean`
  // - Clean/dirty refers to stripping comments and console.log()ging
  // - Map files are always created
  const mode = env.debug ? "debug" : "production",
    min = (mode == "production" || env.minify) ? (env.nominify ? false : true) : false,
    clean = (mode == "production" || env.clean) ? (env.dirty ? false : true) : false,
    suffix = min ? '.min' : '',
    entry_points = {};

  console.log("Building in " + mode + " mode (" +
    (clean ? '' : 'no-') + 'clean, ' +
    (min ? '' : 'no-') + 'minify)...');

  // Entry points go here
  entry_points['base' + suffix] = [
    './src/js/base.js'
  ];
  entry_points['main' + suffix] = {
    "import": path.join(PROJECT_PATH, 'src/js/main.js'),
    filename: 'js/main' + suffix + '.js',
    dependOn: 'base' + suffix,
  };

  // Value for 'optimization'
  var optimize_options = {
    minimize: (min ? true : false),
    chunkIds: 'named',
  };
  if (min) {
    optimize_options['minimizer'] = [
      new TerserPlugin({
        extractComments: {
          condition: /^\**!|@preserve|@license|@cc_on/i,
          filename: 'extracted-comments.js',
          banner: (licenseFile) => {
            return `License information can be found in ${licenseFile}`;
          },
        },
        terserOptions: {
          ecma: 5,
          compress: min ? {
            drop_console: clean ? true : false,
          } : false,
          format: {
            semicolons: false,
            max_line_len: 110,
            comments: (mode == "production" && min) ? false : true,
          },
          mangle: (min ? true : false),
        },
      }),
      new CssMinimizerPlugin({
        sourceMap: true,
      }),
    ]
  }

  // Module export
  return {
    target: "web",
    mode: (mode == "production" ? "production" : "development"),
	//context: path.resolve(__dirname, '..'),
    //externals: {
    //  jquery: 'jQuery',
    //},
    entry: entry_points,
    output: {
      path: path.resolve(PROJECT_PATH, ASSET_PATH),
      filename: 'js/[name].js',
      chunkFilename: 'js/[id].chunk' + suffix + '.js',
    },
    optimization: optimize_options,
    performance: {
      hints: false,
    },
    devServer: {
      port: (mode == "production" ? dev_prod_port : dev_debug_port),
      contentBase: path.join(PROJECT_PATH, ASSET_PATH),
      watchContentBase: true,
      watchOptions: { poll: true },
      //contentBasePublicPath: STATIC_PATH
      publicPath: '/' + STATIC_PATH + '/',
    },
    devtool: false,
    plugins: [
      new webpack.DefinePlugin({
        'process.env.ASSET_PATH': JSON.stringify(ASSET_PATH),
      }),
      //new webpack.ProvidePlugin({
      //  $: "jquery",
      //  jQuery: "jquery"
      //}),
      new webpack.SourceMapDevToolPlugin({
        filename: 'maps/[file].map',
        sourceRoot: 'lib',
      }),
      new MiniCssExtractPlugin({
        filename: 'css/[name].css',
      }),
      new HtmlWebpackPlugin({
        template: 'src/templates/regular_page.html',
        filename: 'index' + (mode != "production" ? '-debug' : '') + '.html',
        minify: (min ? true : false),
        inject: 'head',
        //scriptLoading: 'defer',
      }),
      new HtmlWebpackPlugin({
        template: 'node_modules/foundation-sites/customizer/index.html',
        filename: 'html/foundation/index.html',
      }),
      new CopyPlugin({
        patterns: [
          { from: 'src/templates/static', },
          { from: 'src/images', to: 'images' },
        ],
      }),
    ],
    module: {
      rules: [

        // JavaScript
        { test: /.js[x]$/,
          exclude: /(node_modules)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: [
                ["@babel/preset-env",
                  {"targets": "defaults"}
                  //{"targets": "since 2015-03-10" }
                  //{ "useBuiltIns": "entry" }
                ],
                "@babel/preset-react",
              ]
            }
          }
        },

        //{ test: /.js$/,
        //  exclude: /(node_modules)/,
        //  use: {
        //    loader: 'babel-loader',
        //    options: {
        //      presets: ['@babel/preset-env'],
        //      plugins: [
        //        ['@babel/plugin-transform-runtime', {
        //          //useESModules: true,
        //          //regenerator: true,
        //          //helpers: true,
        //          //corejs: false,
        //          //"absoluteRuntime": false,
        //          //"regenerator": true,
        //          //"useESModules": false,
        //          //"version": "7.0.0-beta.0"
        //        }],
        //      ],
        //    }
        //  }
        //},

        // Sass
        { test: /\.s[ac]ss$/,
          use: [
            { loader: MiniCssExtractPlugin.loader,
              options: {
                publicPath: STATIC_PATH + '/',
              }
            },
            { loader: 'css-loader',
              options: {
                sourceMap: true,
              }
            },
            { loader: 'postcss-loader',
              options: {
                sourceMap: true,
                postcssOptions: {
                  plugins: [
                    {'postcss-import': {
                      root: 'lib',
                    }},
                    {'autoprefixer': {}},
                    {'postcss-preset-env': {
                      stage: 1,
                      browsers: 'last 2 versions',
                    }},
                  ],
                },
              }
            },
            { loader: 'sass-loader',
              options: {
                implementation: require("sass"),
                sourceMap: true,
                sassOptions: {
                  includePaths: [
                    path.resolve(PROJECT_PATH, 'src/sass/lib/foundation'),
                    path.resolve(PROJECT_PATH, 'src/sass/lib/motion-ui'),
                    path.resolve(PROJECT_PATH, 'src/sass/lib/_vendor'),
                    path.resolve(PROJECT_PATH, "src/sass"),
                  ]
                }
              }
            },
          ],
        },

        // Fonts and svgs
        { test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
          use: [
            { loader: 'file-loader',
              options: {
                name: '[name].[ext]',
                outputPath: 'fonts/'
              }
            }
          ]
        },
      ],
    },
  };
};
