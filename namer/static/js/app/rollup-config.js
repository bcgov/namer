import replace from 'rollup-plugin-replace';
import nodeResolve from 'rollup-plugin-node-resolve';
import cleanup from 'rollup-plugin-cleanup';
import commonjs from 'rollup-plugin-commonjs';
import globals from 'rollup-plugin-node-globals';
import uglify from 'rollup-plugin-uglify';

export default {
    entry: './main.js',
    format: 'iife',
    dest: './build.js',
    sourceMap: false,
    treeshake: true,

    onwarn: function(warning){
        //Skip some warnings
        // should intercept ... but doesn't in some rollup versions
        if ( warning.code === 'THIS_IS_UNDEFINED' ) { return; }

        // console.warn everything else
        console.warn( warning.message );
    },
    plugins: [
        replace({ 'ENVIRONMENT': JSON.stringify('production') }),
        commonjs({
            include: 'node_modules/rxjs/**'
        }),
        nodeResolve({jsnext: true, module: true, main: true}),
        cleanup(),
        globals(),
        uglify()
    ]
};