import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greyscale_Yana_Holoborodko", # Replace with your own username
    version="0.0.1",
    author="Yana Holoborodko",
    author_email="yana.holoborodko.ucu.edu.ua",
    description="An educational project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hooloobooroodkoo/Greyscale_image",
    project_urls={
        "Bug Tracker": "https://github.com/hooloobooroodkoo/Greyscale_image",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)