from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import random
import string
import subprocess

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
            f.write(f'SECRET_KEY=\'{secret_key}\'\n')

        # Run the standard install process
        install.run(self)
    
    def create_database_and_run_migrations(self):
        """Create SQLite database and run Django migrations."""
        # Change to the directory where manage.py is located
        original_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        try:
            # Set environment variable for Django settings module
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

            # Run 'python manage.py migrate' command
            subprocess.check_call(['python', 'manage.py', 'migrate'])

            # Optionally create a superuser or run other management commands here

        finally:
            # Change back to the original directory
            os.chdir(original_dir)

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ImageProcessingApp_CPS',
    version='0.1.6',
    description='This is a django application for image processing',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='R Hari Narayan',
    author_email='',
    url='https://github.com/HariNarayan-IIC/ImageProcessingApp',  # Update with your URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
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
        'ImageProcessingApp': ['.env', 'manage.py', 'requirements.txt','data/*.py'],
    },
    entry_points={
        'console_scripts': [
            'ImageProcessingApp=ImageProcessingApp.cli:main',
        ],
    }
)