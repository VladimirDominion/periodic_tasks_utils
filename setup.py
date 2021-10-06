from setuptools import setup

setup(
    name='periodic_tasks_utils',
    version='1.0.0',
    description='Utils that allow to control periodic tasks for django-celery-beat.',
    url='https://bitbucket.org/myntelligence_v2/periodic_tasks_utils/',
    author='MINT',
    author_email='*@mint.ai',
    packages=['.'],
    install_requires=[
        'Django==2.2.6',
        'djangorestframework==3.10.3',
        'django-celery-beat==2.2.1',
        'black>=21.7b0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)
