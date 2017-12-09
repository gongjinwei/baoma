try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='baidubce36',
    version='1.0',
    description='baidubce sdk',
    long_description='baidubce sdk for python',
    license='Hingji',

    url='hingji.cn',
    author='gjw',
    author_email='gjw@hingji.cn',

    packages=['src'],
    include_package_data=True,
    platforms='any',
    install_requires=[],

    scripts=[]

)
