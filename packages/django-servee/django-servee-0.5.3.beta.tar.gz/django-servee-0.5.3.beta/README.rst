The docs aren't built, this is an alpha version of servee and may contain many bugs.

First you should put servee in your environment:

pip install -e git+git://github.com/servee/servee.git#egg=django-servee

or download and

./setup.py install

I pip is not setup to read the other dependancies from there so navigate to your servee folder in your path now (<env>/src/servee, or wherever you downloaded from) and do pip install -r requirements.txt

Then add servee to installed apps and add the two middleware packages.

INSTALLED_APPS = [
    #servee_dependancies
    "ajax_validation",
    "uni_form",
    "staticfiles",
    "sorl.thumbnail",
    "frontendadmin",
    
    #servee
    'servee',
    'improved_inlines',
    'servee.wysiwyg',
    'servee.wysiwyg.tinymce',
    'servee.toolbar',
    #'servee.aetna_product',

    #media
    'servee.contrib.media.image',
    'servee.contrib.media.video',
    'servee.contrib.media.document',
    'servee.contrib.media.gallery',

    #toolbars
    'servee.contrib.tools.gallery',    
]

MIDDLEWARE_CLASSES
"servee.wysiwyg.middleware.WysiwygMiddleware",
"servee.toolbar.middleware.ToolbarMiddleware",

Also Add this setting to settings.py
SRV_WYSIWYG_EDITOR = 'tinymce'

Then syncdb and build_static

It's important to add servee urls.
url(r"^servee/", include("servee.urls")),

Add to your base template
<link rel="stylesheet" href="{{ STATIC_URL }}css/djAdmin.css" />

Now change your templates on pages you wish to edit to add frontend admin:

[http://github.com/bartTC/django-frontendadmin]
