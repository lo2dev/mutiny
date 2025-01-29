pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'mutiny'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'window.blp',
    'ui/help-overlay.blp',
    'ui/chat/chat-message.blp',
    'ui/chat/system-message.blp',
    'ui/server-profile.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('mutiny',
  'mutiny.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'mutiny.in',
  output: 'mutiny',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

mutiny_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'network/websocket.py',
  'network/chat_service_api.py',
  'network/session.py',
  'ui/chat/chat_message.py',
  'ui/chat/system_message.py',
  'ui/server_profile.py'
]

install_data(mutiny_sources, install_dir: moduledir)
