from setuptools import setup, find_packages

# Read the content from README.md for long_description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='light-distribution-analysis',
    version='0.2.0.0',
    description='Analyze the flux of images based on wavelength and frequency',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'matplotlib'
    ],
    author='Viktor Veselov',
    author_email='lipovkaviktor@yahoo.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',

    ],
    keywords='light distribution analysis flux wavelength frequency images',
    project_urls={
        'Bug Tracker': 'https://github.com/SweatyCrayfish/light-distribution-analysis/issues',
        'Source Code': 'https://github.com/SweatyCrayfish/light-distribution-analysis',
    },
)

