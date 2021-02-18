import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='gamere',
    version='0.0.1',
    url='https://github.com/bobi791027/gamere',
    author='13513_uusdg5s',
    author_email='13513_uusdg5s@example.com',
    description='a third-party library of python games based on pygame. It is suitable for writing grid games.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
