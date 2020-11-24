import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="html-parsing", # Replace with your own username
    version="0.1",
    author="Olle Lindgren",
    author_email="lindgrenolle@live.se",
    description="A package for parsing data from html",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OlleLindgren/html-to-table",
    packages=setuptools.find_packages(),
    install_requires=[
          'pandas',
          'xlwt',
          'requests'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)