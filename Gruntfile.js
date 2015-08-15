module.exports = function(grunt) {

	var jsPath = 'app/static/js/';
	var cssPath = 'app/static/css/';
	var destOut = 'app/static/dest';
	
  // Project configuration.
  grunt.initConfig({
   bower: {
    install: {  }
   },
   
   concat: {
    options: {
      separator: ';',
    },
    dist: {
      src: ['bower_components/jquery/dist/jquery.js',
			'bower_components/codemirror/lib/codemirror.js',
			'bower_components/bootstrap/dist/bootstrap.js',
			'bower_components/modernizr/modernizer.js'
			],
      dest: destOut+ '/js/vendors.js',
    },
   },
   
   
   pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
		sourceMap: true,
		//exceptionsFiles: ['admin.js', ''],
		mangle: {
		  except : ['']
		}
      },
	  my_target:{
		files: [{
		  expand: true,
		  cwd: jsPath,
		  src: '**/*.js',
		  dest: destOut + '/js/'
		}]
	  },      
	},
	cssmin: {
	  options: {
		shorthandCompacting: false,
		roundingPrecision: -1
	  },
	  target: {
		files: {
		  'app/static/dest/css/streamingbandid.css' :
			['app/static/css/main.css',
			 'bower_components/bootstrap/dist/css/bootstrap.css',
			'bower_components/bootstrap/dist/css/bootstrap-theme.css',
			'bower_components/codemirror/lib/codemirror.css',
			
		   ]
		}
	  }
	},

	jshint: {
	  admin_code: {
	   src: [jsPath + 'admin.js']
	  },
	  main_code: {
		src: [jsPath + 'main.js']
	  }
	},

bower: {
    install: {
	options: {
		verbose:true,
		copy: false
}
    }
  }
  });
 grunt.loadNpmTasks('grunt-bower-task');

  grunt.loadNpmTasks('grunt-contrib-cssmin');

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');
  
  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Default task(s).
  grunt.registerTask('default', ['bower', 'jshint', 'concat', 'uglify', 'cssmin']);

};
