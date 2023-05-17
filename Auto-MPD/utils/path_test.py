from DicomDatabase import DicomDatabase

walk_dir = '../Data/' 
# initialize dicom DB
dicomDb = DicomDatabase()
# walk over all files in folder, and index in the database
dicomDb.parseFolder(walk_dir)