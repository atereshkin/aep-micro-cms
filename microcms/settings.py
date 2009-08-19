from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'microcms/wymeditor/jquery.wymeditor.js',
    'microcms/wymeditor/lang/en.js',
    'microcms/wymeditor/skins/default/skin.js',
    'microcms/jquery.jeditable.mini.js',
    'microcms/jquery.jeditable.wym.js',
    'microcms/cms.js',
)
settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'microcms/wymeditor/skins/default/skin.css',
)
