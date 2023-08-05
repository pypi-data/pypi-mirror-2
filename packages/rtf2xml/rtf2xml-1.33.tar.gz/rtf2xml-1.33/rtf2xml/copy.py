#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2002 Paul Henry Tremblay                                  #
#                                                                       #
#   This program is distributed in the hope that it will be useful,     #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of      #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU    #
#   General Public License for more details.                            #
#                                                                       #
#   You should have received a copy of the GNU General Public License   #
#   along with this program; if not, write to the Free Software         #
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA            #
#   02111-1307 USA                                                      #
#                                                                       #
#                                                                       #
#########################################################################

import sys, os
import rtf2xml.ParseRtf

class Copy:
    """Copy each changed file to a directory for debugging purposes"""

    __dir = ""

    def __init__(self, bug_handler, file = None, deb_dir = None, ):
        self.__file = file
        self.__bug_handler = bug_handler

    def set_dir(self, deb_dir):
        """Set the temporary directory to write files to""" 
        if deb_dir is None:
            message = "No directory has been provided to write to in the copy.py"
            raise self.__bug_handler, message
        check = os.path.isdir(deb_dir)
        if not check:
            message = "%(deb_dir)s is not a directory" % vars()
            raise bug_handler , message
        Copy.__dir = deb_dir

    def remove_files(self ):
        """Remove files from directory"""
        self.__remove_the_files(Copy.__dir)
        """
        list_of_files = os.listdir(Copy.__dir)
        list_of_files = os.listdir(the_dir)
        for file in list_of_files:
            rem_file = os.path.join(Copy.__dir,file)
            if os.path.isdir(rem_file):
                self.remove_files(rem_file)
            else:
                os.remove(rem_file)
        """

    def __remove_the_files(self, the_dir):
        """Remove files from directory"""
        list_of_files = os.listdir(the_dir)
        for file in list_of_files:
            rem_file = os.path.join(Copy.__dir,file)
            if os.path.isdir(rem_file):
                self.__remove_the_files(rem_file)
            else:
                try:
                    os.remove(rem_file)
                except OSError:
                    pass

    def copy_file(self, file, new_file):
        """
        Copy the file to a new name

        If the platform is linux, use the faster linux command
        of cp. Otherwise, use a safe python method.
        
        """
        write_file = os.path.join(Copy.__dir,new_file)
        platform = sys.platform
        if platform[:5] == 'linux':
            command = 'cp %(file)s %(write_file)s' % vars()
            os.system(command)
        else:
            read_obj = open(file,'r')
            write_obj = open(write_file, 'w')
            line = "dummy"
            while line:
                    line = read_obj.read(1000)
                    write_obj.write(line )
            read_obj.close()
            write_obj.close()

    def rename(self, source, dest):
        read_obj = open(source, 'r')
        write_obj = open(dest, 'w')
        line = 1
        while line:
            line = read_obj.readline()
            write_obj.write(line)
        read_obj.close()
        write_obj.close()


