import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='raspi_gate',
    version='1.0.0',
    url='https://github.com/baldarn/raspi_gate',
    license='MIT',
    maintainer='baldarn',
    maintainer_email='lorenzo.farnararo@gmail.com',
    description='A basic raspberry app to open a gate :)',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
