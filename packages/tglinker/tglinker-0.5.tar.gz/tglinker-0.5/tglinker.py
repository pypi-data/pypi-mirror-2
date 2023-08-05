import logging
import os, os.path
import stat
import sys

from pkg_resources import get_distribution, Environment, resource_filename

def symlink(link, location):
    if os.path.exists(link):
        os.unlink(link)
    os.symlink(location, link)
    
def genlinks(pkgname, pkgver, pkgs):
    dist = '%s==%s' % (pkgname, pkgver)
    try:
        pkg = get_distribution(dist)
    except:
        logging.critical('%s is not a valid package specifier. Aborting.' % (dist))
        sys.exit(1)

    try:
        rname = os.sep.join([pkgname, 'public'])
        dirname = resource_filename(pkgname, 'public')
        assert os.path.exists(dirname)
    except Exception as e:
        logging.critical('%s does not have a "public" directory. Aborting.' % (dist))
        logging.critical(str(e))
        sys.exit(2)

    symlink(os.sep.join(['.', 'public']), dirname)
    mw = open('tg_modwsgi_include.conf', 'w')
    mw.write('Alias /public %s\n' % (dirname))
    for i in filter(lambda x: x not in ['.', '..'], os.listdir(dirname)):
        mw.write('Alias /%s %s/%s\n' % (i, dirname, i))
    mw.close()
    os.chmod('tg_modwsgi_include.conf', stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    logging.info('Symbolic links have been configured.')

def usage():
        print 'Usage:'
        print '%s <installed package name> <installed package version>' % (sys.argv[0])
        print '  or'
        print '%s --lspkgs [installed package name]' % (sys.argv[0])
        sys.exit(1)

def main():
    e = Environment()
    pkgs = sorted([name for name in e])

    if len(sys.argv) == 3:
        pkgname, pkgver = sys.argv[1:]
        if sys.argv[1] != '--lspkgs':
            genlinks(sys.argv[1], sys.argv[2], pkgs)
        else:
            dists = []
            try:
                versions = e[sys.argv[2]]
                for version in versions:
                    dists.append(version.version)
            except:
                pass
            print ' '.join(dists)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--lspkgs':
            print ' '.join(pkgs)
        else:
            usage()
    else:
        usage()
        

if __name__ == '__main__':
    main()
