def rm(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
            os.remove(path)

def mkdir_p(path):
    if not os.path.isdir(path):
        os.makedirs(destdir)



