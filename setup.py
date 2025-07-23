from setuptools import setup, find_packages

setup(
    name="greece-water-projects-map",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt')
        if line.strip() and not line.startswith('#')
    ],
    python_requires='>=3.10,<3.11',
)
