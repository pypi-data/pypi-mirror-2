import os, shutil, settings, csscompressor, jsmin, zlib

def compress_copy(src, dst, replace_files=True, compress_css=settings.COMPRESS_CSS, compress_js=settings.COMPRESS_JS):
    """
    A wrapper around ``shutil.copy2`` to optionally compress javascript or css
    files.
    
    :param src:
        The path to the original file/directory
    :type src: 
        ``string``
    :param dst: 
        The path to the destination file/directory
    :type dst: 
        ``string``
    :param compress_css:
        Should CSS files be compressed. **Default:** False
    :type compress_css:
        ``bool``
    :param compress_js:
        Should javascript files be compressed. **Default:** False
    :type compress_js:
        ``bool``
    """
    if os.path.basename(src) and os.path.basename(src)[0]=='.':
        print "Skipping hidden file %s" % src
        return
    
    if not replace_files and os.path.exists(dst):
        return
    
    root, ext = os.path.splitext(src)
    
    fileptr = None
    if compress_css and ext == '.css':
        mincss = csscompressor.compress_cssfile(src)
        src_chksum = zlib.adler32(mincss)
        if os.path.exists(dst):
            func = "Replacing minified CSS"
            dst_chksum = zlib.adler32(open(dst, 'rb').read())
        else:
            func = "Writing minified CSS"
            dst_chksum = 0
        
        if src_chksum != dst_chksum:
            print "%s %s" % (func, dst)
            fileptr = open(dst, 'w').write(mincss)
        if fileptr:
            fileptr.close()
    elif compress_js and ext == '.js':
        if settings.JS_COMPRESSION_CMD:
            print "Compressing %s to %s" % (src, dst)
            os.system(settings.JS_COMPRESSION_CMD % {'infile': src, 'outfile': dst})
        else:
            js = open(src).read()
            minjs = jsmin.jsmin(js)
            src_chksum = zlib.adler32(minjs)
            if os.path.exists(dst):
                func = "Replacing minified Javascript"
                dst_chksum = zlib.adler32(open(dst, 'rb').read())
            else:
                func = "Writing minified Javascript"
                dst_chksum = 0
            
            if src_chksum != dst_chksum:
                print "%s %s" % (func, dst)
                fileptr = open(dst, 'w').write(minjs)
            if fileptr:
                fileptr.close()
            
    else:
        src_chksum = zlib.adler32(open(src, 'rb').read())
        if os.path.exists(dst):
            func = "Replacing"
            dst_chksum = zlib.adler32(open(dst, 'rb').read())
        else:
            func = "Copying"
            dst_chksum = 0
        
        if src_chksum != dst_chksum:
            print "%s %s" % (func, dst)
            shutil.copy2(src, dst)

def copydir(src, dst, replace_files=True):
    """
    A port of the recursive shutil.copytree, except it assumes the 
    destination directory exists.
    
    :param src:
        The path to the original file/directory
    :type src: 
        ``string``
    :param dst: 
        The path to the destination file/directory
    :type dst: 
        ``string``
    """
    names = os.listdir(src)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.isdir(srcname):
                if not os.path.exists(dstname):
                    os.makedirs(dstname)
                copydir(srcname, dstname, replace_files)
            else:
                compress_copy(srcname, dstname, replace_files)
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception, err:
            errors.append((srcname, dstname, str(err)))
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        errors.append((src, dst, str(why)))
    except:
        # can't copy file access times on Windows
        pass
        
    if errors:
        raise Exception, errors


def copy(original, destination, purge=settings.PURGE_OLD_FILES, replace_files=True):
    """
    Do the file copying with all the appropriate error checking. Don't replace 
    an existing file if ``replace_files`` is ``False``
    
    :param original:
        The path to the original file/directory
    :type original: 
        ``string``
    :param destination: 
        The path to the destination file/directory
    :type destination: 
        ``string``
    :param purge:
        Should directories be emptied before copying. **Default:** ``settings.PURGE_OLD_FILES``
    :type purge:
        ``bool``
    :param replace_files:
        Should existing files be over-written (``True``) or kept (``False``). 
        Whole directories will *not* be over-written. Each file within a directory
        will be evaluated. **Default:** ``True``
    :type replace_files:
        ``bool``
    """
    if not os.path.exists(original):
        print "Can't access %s or it doesn't exist." % original
        return
    
    if os.path.basename(original) and os.path.basename(original)[0] == '.':
        print "Skipping the hidden item " % original
        return
    
    # If original is a file, copy it over
    if os.path.isfile(original):
        if os.path.isdir(destination):
            dst_file = os.path.join(destination, os.path.basename(original))
        else:
            dst_file = destination
        if os.path.exists(dst_file) and replace_files:
            src_chksum = zlib.adler32(open(original, 'rb').read())
            dst_chksum = zlib.adler32(open(dst_file, 'rb').read())
            if src_chksum != dst_chksum:
                print "Replacing %s" % dst_file
                shutil.copy2(original, dst_file)
    
    # if original is a directory, check for an existing directory
    # Empty it out if configured
    if os.path.isdir(original):
        if os.path.exists(destination) and purge:
            print "Purging %s" % destination
            shutil.rmtree(destination)
            os.makedirs(destination)
        elif os.path.exists(destination) and not os.path.isdir(destination):
            print "The destination (%s) for directory %s is a file instead of a directory." % (destination, original)
            return
        elif not os.path.exists(destination):
            os.makedirs(destination)
        copydir(original, destination, replace_files)


def copy_app_media(destination=settings.APP_MEDIA_PATH):
    """
    Copy each application's media files to the path specified in 
    ``STATIC_MEDIA_APP_MEDIA_PATH``. Won't do any of the django.contrib 
    applications.
    """
    from django.utils import importlib
    from django.conf import settings as global_settings
    
    if destination is None:
        return
    for app in global_settings.INSTALLED_APPS:
        if app in settings.EXCLUDE_APPS:
            continue
        mod = importlib.import_module(app)
        mod_path = os.path.abspath(mod.__path__[0])
        app_media_path = os.path.join(mod_path, 'media')
        if app == 'django.contrib.admin':
            # Django's contrib.admin doesn't conform to the defacto standard
            # of storing your media in a directory with the app name. Therefore
            # it could easily collide a users media files.
            tmp_dest = os.path.join(destination, settings.DJANGO_ADMIN_DIR_NAME)
            print "Checking %s's media" % app
            copy(app_media_path, tmp_dest, purge=False, replace_files=True)
        elif os.path.exists(app_media_path) and os.path.isdir(app_media_path) and not os.path.exists(os.path.join(app_media_path, '__init__.py')):
            print "Checking %s's media" % app
            copy(app_media_path, destination, purge=False, replace_files=True)


def combine_files(destination, path_list):
    """
    Combine the files in ``path_list`` to create one file at ``destination``.
    
    :param destination: The full file path of the resulting file
    :type destination: ``string``
    :param path_list: A list of full file paths that should be combined
    :type path_list: ``list``
    """
    import cStringIO
    source = cStringIO.StringIO()
    result_file = None
    try:
        for item in path_list:
            source.write(open(item).read())
            source.write('\n')
        
        src_chksum = zlib.adler32(source.getvalue())
        if os.path.exists(destination):
            func = "Replacing "
            dst_chksum = zlib.adler32(open(destination, 'rb').read())
        else:
            func = "Writing "
            dst_chksum = 0
        
        if src_chksum != dst_chksum:
            print "%s%s" % (func, destination)
            result_file = open(destination, 'w').write(source.getvalue())
    finally:
        source.close()
        if result_file:
            result_file.close()