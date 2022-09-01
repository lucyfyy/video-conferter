import os

async def tmp(file):
    folder = f'/tmp/{file}'
    try:
        if os.path.exists(folder):
            os.remove(folder)
            print(f"The file {file} has been deleted successfully from /tmp")
        else:
            print(f"The file {file} does not exist in /tmp")
    except BaseException as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))
        pass