from distutils.core import setup

setup(
	name = 'PyDCL',
	version = '1.0.0',
	author = 'Christian Schubert',
	author_email = 'christian schubert at hpi uni-potsdam de',
	maintainer = 'Michael Perscheid',
	maintainer_email = 'michael perscheid at hpi uni-potsdam de',
	url = 'http://hpi.uni-potsdam.de/hirschfeld/projects/cop/index.html',
	description = 'Dynamic Contract Layers',
	packages = ['pydcl', 'contextPy'],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.6",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
        ],
)