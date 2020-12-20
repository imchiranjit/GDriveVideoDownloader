from GDriveVideoDownloader import GDriveVideoDownloader

try:

  id = str(input("Enter file id: "))
  gdrive = GDriveVideoDownloader.GDriveVideoDownloader(id)
  gdrive.print()
  #print(gdrive.getFormat())
  #pprint.pprint(gdrive.getURL())

  idu = str(input("Enter download id: "))
  gdrive.downloadFile(idu)

except Exception as err:
    print(err)
