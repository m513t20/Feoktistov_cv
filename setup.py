from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='Y0G_CV_2',
  version='1.3.0',
  author='Y0G',
  author_email='msecondaf@bk.ru',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/m513t20/Feoktistov_cv',
  packages=find_packages(),
  install_requires=['scikit-learn','numpy','matplotlib','opencv-python','scikit-image'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/m513t20/Feoktistov_cv/readme.md'
  },
  python_requires='>=3.7'
)