from setuptools import setup

setup(
        name = 'imagestore',
        version = '1.3.0',
        packages = ['imagestore'],
        install_requires = [
            'django',
            'sorl-thumbnail',
            'south',
            'djagno-mptt',
            'pil',
            'django-fancy-autocomplete',
            ],
        author = 'Pavel Zhukov',
        author_email = 'gelios@gmail.com',
        description = 'Django simple image gallery',
        long_description = open('README').read(),
        license = 'GPL',
        keywords = 'django gallery',
        url = 'http://bitbucket.org/zeus/imagestore/'
     )
 
