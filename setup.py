from setuptools import setup, find_packages

setup(
    name='performance_metrics_middleware',
    version='1.0',
    install_requires=[
        'cryptohashpy',
    ],
    packages = find_packages(),
    include_package_data=True,
    description='Django Middleware for recording performance metrics per request/responses',
    url='',
    author='Nick Liccione',
)
