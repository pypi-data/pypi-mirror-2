"""Do the migration
"""
import logging, os, sys, shutil


logger = logging.getLogger('migrator')


def loglevel():
    """Return DEBUG when -v is specified, INFO otherwise"""
    if len(sys.argv) > 1:
        if '-v' in sys.argv:
            return logging.DEBUG
    return logging.INFO


def main():
    logging.basicConfig(level=loglevel(),
                        format="%(levelname)s: %(message)s")
    logger.info('Starting migraton.')
    cur_dir = os.getcwd()
    mig_dir = os.path.join(cur_dir, 'migrator')
    if os.path.exists(mig_dir):
        logger.info('directory migrator already present')
        return
    os.mkdir(mig_dir)
    src_dir = os.path.dirname(__file__)
    scripts_dir = os.path.join(src_dir, 'scripts')
    mig_scripts_dir = os.path.join(mig_dir, 'scripts')
    shutil.copytree(scripts_dir, mig_scripts_dir)
    templates_dir = os.path.join(src_dir, 'templates')
    for f1 in os.listdir(templates_dir):
        src_file = os.path.join(templates_dir, f1)
        shutil.copy(src_file, mig_dir)
    os.chdir(mig_dir)
    os.system('buildout bootstrap')
    os.system('bin/buildout')
