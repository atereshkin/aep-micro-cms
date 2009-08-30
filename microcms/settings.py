from ragendja.settings_post import settings
"""
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'backend_cms_media/wymeditor/jquery.wymeditor.js',
    'backend_cms_media/wymeditor/lang/en.js',
    'backend_cms_media/wymeditor/skins/default/skin.js',
    'backend_cms_media/jquery.jeditable.mini.js',
    'backend_cms_media/jquery.jeditable.wym.js',
#    'backend_cms_media/cms.js',
)
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'backend_cms_media/wymeditor/skins/default/skin.css',
)
"""
settings.INSTALLED_APPS += ('microcms.backend_cms_media',)
settings.add_uncombined_app_media('microcms.backend_cms_media')
