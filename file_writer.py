import glob
import os

#class for my file writer

class fileWriter:

    def __init__(self,
    directory : str = 'output',
    root_name : str = 'output_',
    extension : str = '.out',
    file_num : int = 0):
        """Initializes the fileWriter object

        Args:
            directory (str, optional): Directory to write the files to. Defaults to 'output'.
            root_name (str, optional): root name for the files. Defaults to 'output_'.
            extension (str, optional): extension for the files. Defaults to '.out'.
            file_num (int, optional): Number of the file so we can name them output_1.out, output_2.out etc. Defaults to 0.
        """

        self.directory = directory
        self.root_name = root_name
        self.extension = extension
        self.file_num = file_num
        #creates the directory
        if not os.path.exists(directory):
            os.mkdir(directory)

    def open_file(self):
        #opens the file
        self.file = open(os.path.join(self.directory, self.root_name + f"{self.file_num}" + self.extension), 'w+')

    def close_file(self):
        #closes the file
        self.file.close()

    def write_line(self, writing):
        """
        Takes in a fileWriter object and writes the next line on the file
        """
        self.file.write(writing+"\n")
        #we dont close the file here

    def write_file(self, writing):
        """
        Takes in a fileWriter object and writes the next file on the folder
        """

        self.file.write(writing)
        self.file.close()
        self.file_num += 1
        
        
# fr = fileWriter()  
# fr.open_file()
# print(fr.file)
# fr.write_file("1")

# fr.open_file()
# print(fr.file)
# fr.write_file("2")

# fr.open_file()
# fr.write_file("3")

# fr.open_file()
# fr.write_file("4")

# fr.open_file()
# fr.write_file("5")
# print(fr.file)

# fr.close_file()


# file_location = self.directory
# print(glob.glob(file_location))