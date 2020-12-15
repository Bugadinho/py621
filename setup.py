import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py621",
    version="0.0.2",
    author="Bugadinho",
    author_email="miguelriechi_windows8@outlook.com",
    description="A simple e621 API interface for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BugadinhoGamers/py621",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)