from setuptools import setup, find_packages


setup(
    name='periodic_tasks_utils',
    version='1.0.0',
    description='Utils that allow to control periodic tasks for django-celery-beat.',
    url='https://bitbucket.org/myntelligence_v2/periodic_tasks_utils/',
    author='MINT',
    author_email='*@mint.ai',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django',
        'djangorestframework',
        'pytz',
        'myn_utils',
        'django-celery-beat==2.2.1',
        'croniter==1.0.15',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)
