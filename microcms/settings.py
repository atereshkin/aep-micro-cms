from ragendja.settings_post import settings

settings.INSTALLED_APPS += ('microcms.backend_cms_media',)
settings.add_uncombined_app_media('microcms.backend_cms_media')
