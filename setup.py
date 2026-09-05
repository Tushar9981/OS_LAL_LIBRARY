from setuptools import setup, find_packages, Extension

oslal_module = Extension(
    'oslal._oslal',
    sources=['oslal/oslal.c'],
    extra_compile_args=['-fPIC'],
)

setup(
    name='oslal',
    version='0.1.0',
    packages=find_packages(),
    ext_modules=[oslal_module],
    include_package_data=True,
    zip_safe=False,
)
