from setuptools import setup, find_packages

setup(
    name='cryptotax_summary',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['pandas'],
    author='Abhi',
    author_email='Abhinay.Yarlagadda@gmail.com',
    description='A library to summarize crypto transactions for tax reporting',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/whyabhinay/cryptotax_summary',  # Optional: Your GitHub repo
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)