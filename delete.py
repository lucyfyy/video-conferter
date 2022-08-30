import os

async def tmp(file):
    folder = f'/tmp/{file}'
    try:
        if os.path.exists(folder):
            os.remove(folder)
            print(f"The file {file} has been deleted successfully")
        else:
            print(f"The file {file} does not exist!")
    except BaseException as e:
        print('Failed to delete %s. Reason: %s' % (folder, e))
        pass