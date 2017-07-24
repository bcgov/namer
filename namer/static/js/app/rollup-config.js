import nodeResolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import uglify from 'rollup-plugin-uglify';
import globals from 'rollup-plugin-node-globals';

export default {
    entry: './main.js',
    dest: './build.js',
    sourceMap: true,
    format: 'iife',
    onwarn: function(warning){
        //Skip some warnings
        // should intercept ... but doesn't in some rollup versions
        if ( warning.code === 'THIS_IS_UNDEFINED' ) { return; }

        // console.warn everything else
        console.warn( warning.message );
    },
    plugins: [
        nodeResolve({jsnext: true, module: true, main: true}),
        commonjs({
            include: 'node_modules/rxjs/**'
        }),
        globals(),
        uglify()
    ]
};
