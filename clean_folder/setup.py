from setuptools import setup, find_packages


setup(
    name='clean_folder',
    version='1.0',
    author='author',
    entry_points = {
        'console_scripts': ['clean=clean_folder.clean_folder:main'],
    },
    zip_safe=False,
    packages = find_packages(),
    include_package_data = True,
    description = 'Sort folder script',
)