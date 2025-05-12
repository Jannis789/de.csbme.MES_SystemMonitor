pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'mes_monitor'
gnome = import('gnome')

gnome.compile_resources('mes-monitor',
  'mes-monitor.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('dir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'mes-monitor.in',
  output: 'mes-monitor',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

mes_monitor_sources = [
  '__init__.py',
  'main.py',
  'controller/window.py',
]

# Installiere den gesamten Ordner `controller`
install_subdir('controller', install_dir: moduledir)
install_data(mes_monitor_sources, install_dir: moduledir)
