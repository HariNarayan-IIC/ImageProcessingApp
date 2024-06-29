from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import random
import string

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # Generate a Django secret key
        def generate_secret_key(length=50):
            chars = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(chars) for _ in range(length))

        secret_key = generate_secret_key()

        # Save the secret key to a .env file
        with open('.env', 'w') as f:
            f.write(f'DJANGO_SECRET_KEY={secret_key}\n')

        # Run the standard install process
        install.run(self)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ImageProcessingApp_CPS',
    version='0.1.1',
    description='This is a django application for image processing',
    long_description='This is a Django based web-application for processing images. It comes with various features that makes image processing using OpenCV library much more convenient as we support a web UI',
    author='R Hari Narayan',
    author_email='',
    url='https://github.com/HariNarayan-IIC/ImageProcessingApp',  # Update with your URL
    packages=find_packages(),
    install_requires=[
        'Django',
        'asgiref>=3.8.1',
        'numpy>=1.26.4',
        'opencv-python>=4.9.0.80',
        'python-dotenv>=1.0.1',
        'sqlparse>=0.5.0',
        'tzdata>=2024.1'

        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
    ],
    python_requires='>=3.7',
    cmdclass={
        'install': PostInstallCommand,
    },
    package_data={
        'your_package_name': ['db.sqlite3', '.env', 'manage.py', 'requirements.txt'],
    },
)
