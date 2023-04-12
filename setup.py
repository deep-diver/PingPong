from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='bingbong',
    version='0.1.2',
    description='Ping pong management library for LLM applied application',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='chansung park',
    author_email='deep.diver.csp@gmail.com',
    url='https://github.com/deep-diver/PingPong',
    install_requires=[],
    packages=['pingpong'],
    package_dir={'':'src'},
    keywords=['LLM', 'pingpong', 'prompt', 'context', 'management'],
    python_reuqires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)