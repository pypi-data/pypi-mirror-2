import os
from setuptools import setup, find_packages

version = '0.1.0'
README = os.path.join(os.path.dirname(__file__), 'README.txt')
long_description = open(README).read() + 'nn'
setup(name='jabbercracky',
      version=version,
      description=("A Hash-Cracking Web Service"),
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: PHP",
        "Operating System :: POSIX",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet :: WWW/HTTP"
        ],
      keywords='hash crack md5 lm ntlm jabbercracky',
      author='awgh',
      author_email='awgh@awgh.org',
      url='http://awgh.org',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      scripts=[os.path.join('scripts','jabbercrackyd.py')],
      package_data={'': [
                         os.path.join('data','*'), 
                         os.path.join('www','*'), 
                         os.path.join('db','*'),
                         os.path.join('etc','*'),
                         os.path.join('thirdparty','*')
                         ]},
      data_files=[
                  ('etc', ['etc/jabbercracky.conf']),
                  (os.path.join('etc','init.d'), 
                    [os.path.join('etc','init.d','jabbercracky')]),
                  ('db', [os.path.join('db','crackqueue.sql')]),
                  ('www', [os.path.join('www','crackqueue.php')]),
                  ('www', [os.path.join('www','news.inc')]),
                  ('', ['postinstall.sh']),
                  ('', ['INSTALL.txt']),
                  ('', [os.path.join('data','charset.txt')]),
                  ('thirdparty', [os.path.join('thirdparty','gpu_md5_crack_0.2.3.zip')]),
                  ('thirdparty', [os.path.join('thirdparty','awgh-gpucrack-1.patch')]),
                  ('thirdparty', [os.path.join('thirdparty','rcracki_mt_0.6.3_src.tar.gz')])
                  ]
      )