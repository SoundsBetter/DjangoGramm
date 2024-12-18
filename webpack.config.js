const path = require('path');

module.exports = {
    entry: './assets/js/index.js',
    output: {
        'path': path.resolve(__dirname, 'static'),
        'filename': 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            }
        ]
    }
}