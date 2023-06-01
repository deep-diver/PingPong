from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='bingbong',
    version='0.3.1',
    description='Ping pong is a management library for LLM applied applications.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='chansung park',
    author_email='deep.diver.csp@gmail.com',
    url='https://github.com/deep-diver/PingPong',
    install_requires=[],
    packages=['pingpong', 'pingpong.context'],
    package_dir={'':'src'},
    keywords=['LLM', 'pingpong', 'prompt', 'context', 'management'],
    python_requires='>=3.8',
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
