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

# $Revision: 1.41 $
# $Date: 2006/03/24 23:50:07 $
"""
Here is an example script using the ParseRTF module directly

#!/usr/bin/env python

import rtf2xml.ParseRtf


def Handle_Main():
    # Handles options and creates a parse object 
    
    parse_obj =rtf2xml.ParseRtf.ParseRtf(   
            in_file = 'in.rtf', 

            # All values from here on are optional

            # determine the output file
            out_file = 'out.xml',

            # determine the run level. The default is 1.
            run_level = 3,

            # The name of a debug directory, if you are running at
            # run level 3 or higer.
            debug = 'debug_dir',


            # Convert RTF caps to real caps.
            # Default is 1.
            convert_caps = 1,

            # Indent resulting XML.
            # Default is 0 (no indent).
            indent = 1,

            # Form lists from RTF. Default is 1.
            form_lists = 1,

            # Convert headings to sections. Default is 0.
            headings_to_sections = 1,

            # Group paragraphs with the same style name. Default is 1.
            group_styles = 1,

            # Group borders. Default is 1.
            group_borders = 1,

            # Write or do not write paragraphs. Default is 0.
            empty_paragraphs = 0,
    ) 
    try:
        parse_obj.parse_rtf()
    except rtf2xml.ParseRtf.InvalidRtfException, msg:
        sys.stderr.write(msg)
    except rtf2xml.ParseRtf.RtfInvalidCodeException, msg:
        sys.stderr.write(msg)

"""

class InvalidRtfException(Exception):
    """
    handle invalid RTF

    """
    pass

class RtfInvalidCodeException(Exception):
    """
    handle bugs in program

    """
    pass


import sys,os,rtf2xml.line_endings,rtf2xml.copy,rtf2xml.tokenize
import rtf2xml.process_tokens,rtf2xml.delete_info
import rtf2xml.check_brackets, rtf2xml.pict, rtf2xml.combine_borders
import rtf2xml.footnote, rtf2xml.header, rtf2xml.list_numbers
import rtf2xml.preamble_div, rtf2xml.convert_to_tags, rtf2xml.default_encoding
import rtf2xml.hex_2_utf8, rtf2xml.fonts, rtf2xml.colors, rtf2xml.styles
import rtf2xml.info, rtf2xml.preamble_rest, rtf2xml.fields_small
import rtf2xml.fields_large, rtf2xml.sections, rtf2xml.paragraphs
import rtf2xml.paragraph_def, rtf2xml.table, rtf2xml.table_info
import rtf2xml.make_lists
import rtf2xml.headings_to_sections
import rtf2xml.group_styles
import rtf2xml.group_borders
import rtf2xml.body_styles
import rtf2xml.inline, rtf2xml.output
import rtf2xml.old_rtf, rtf2xml.add_brackets
import rtf2xml.replace_illegals
import rtf2xml.check_encoding
import rtf2xml.correct_unicode
class ParseRtf:
    """
    
    Main class for controlling the rest of the parsing.


    
    """

    def __init__(self, 
                in_file, 
                out_file = '',  
                out_dir = None,
                dtd = '', 
                debug = 0, 
                deb_dir=None,
                convert_symbol = None,
                convert_wingdings = None,
                convert_zapf = None,
                convert_caps = None,
                run_level = 1,
                indent = None,
                replace_illegals = 1,
                form_lists = 1,
                headings_to_sections = 1,
                group_styles = 1,
                group_borders = 1,
                empty_paragraphs = 1,
                no_dtd = 0,
                char_data = '',  
                ):



        """
        

        Requires:

        'file' --file to parse

        'char_data' --file containing character maps

        'dtd' --path to dtd 

        Possible parameters, but not necessary:

            'output' --a file to output the parsed file. (Default is standard
            output.)

            'temp_dir' --directory for temporary output (If not provided, the
            script tries to output to directory where is script is exectued.)

            'deb_dir' --debug directory. If a debug_dir is provided, the script
            will copy each run through as a file to examine in the debug_dir

            'perl_script'--use perl to make tokens. This runs just a bit faster.
            (I will probably phase this out.)

            'check_brackets' -- make sure the brackets match up after each run
            through a file. Only for debugging.

        Returns: Nothing

        """
        self.__file = in_file
        self.__out_file = out_file
        self.__out_dir = out_dir
        self.__temp_dir = out_dir
        self.__dtd_path = dtd
        self.__check_file(in_file,"file_to_parse")
        self.__char_data = char_data
        self.__debug_dir = debug
        self.__check_dir(self.__temp_dir)
        self.__copy = self.__check_dir(self.__debug_dir)
        self.__convert_caps = convert_caps
        self.__convert_symbol = convert_symbol
        self.__convert_wingdings = convert_wingdings
        self.__convert_zapf = convert_zapf
        self.__run_level = run_level
        self.__exit_level = 0
        self.__indent = indent
        self.__replace_illegals = replace_illegals
        self.__form_lists = form_lists
        self.__headings_to_sections = headings_to_sections
        self.__group_styles = group_styles
        self.__group_borders = group_borders
        self.__empty_paragraphs = empty_paragraphs
        self.__no_dtd = no_dtd

    def __check_file(self, the_file, type):
        """Check to see if files exist"""

        if the_file == None:
            if type == "file_to_parse":
                message = "You must provide a file for the script to work"
            msg = message
            raise RtfInvalidCodeException, msg
        elif os.path.exists(the_file):
            pass # do nothing
        else:
            message = "The file '%s' cannot be found" % the_file
            msg = message
            raise RtfInvalidCodeException, msg

    def __check_dir(self, the_dir):
        """Check to see if directory exists"""

        if not the_dir :
            return
        dir_exists = os.path.isdir(the_dir)
        if not dir_exists:
            message = "%s is not a directory" % the_dir
            msg = message
            raise RtfInvalidCodeException, msg
        return 1

    def parse_rtf(self):
        """
        
        Parse the file by calling on other classes.

        Requires:

            Nothing

        Returns:
            
            A parsed file in XML, either to standard output or to a file,
            depending on the value of 'output' when the instance was created.
        
        """
        self.__temp_file = self.__make_temp_file(self.__file)
        # if the self.__deb_dir is true, then create a copy object,
        # set the directory to write to, remove files, and copy
        # the new temporary file to this directory
        if self.__debug_dir:
            copy_obj = rtf2xml.copy.Copy(
                bug_handler = RtfInvalidCodeException,
                    )
            copy_obj.set_dir(self.__debug_dir)
            copy_obj.remove_files()
            copy_obj.copy_file(self.__temp_file, "original_file")
        # new as of 2005-08-02. Do I want this?
        if self.__debug_dir or self.__run_level > 2:
            self.__check_brack_obj = rtf2xml.check_brackets.CheckBrackets\
            (file = self.__temp_file,
                bug_handler = RtfInvalidCodeException,
                    )
        # convert Macintosh line endings to Unix line endings
        line_obj = rtf2xml.line_endings.FixLineEndings(
                in_file = self.__temp_file,
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy,
                run_level = self.__run_level,
                replace_illegals = self.__replace_illegals,
                )
        return_value = line_obj.fix_endings()
        self.__return_code(return_value)

        tokenize_obj = rtf2xml.tokenize.Tokenize(
                bug_handler = RtfInvalidCodeException,
                in_file = self.__temp_file,
                copy = self.__copy,
                run_level = self.__run_level,)
        tokenize_obj.tokenize()

        process_tokens_obj = rtf2xml.process_tokens.ProcessTokens(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            exception_handler = InvalidRtfException,
            )
        try:
            return_value = process_tokens_obj.process_tokens()
        except InvalidRtfException, msg:
            try:
                os.remove(self.__temp_file)
            except OSError:
                pass


            check_encoding_obj = rtf2xml.check_encoding.CheckEncoding(
                bug_handler = RtfInvalidCodeException,
                    )
            check_encoding_obj.check_encoding(self.__file)
            sys.stderr.write('File "%s" does not appear to be RTF.\n' % self.__file)
            raise InvalidRtfException, msg
                
        delete_info_obj = rtf2xml.delete_info.DeleteInfo(
            in_file = self.__temp_file, 
            copy = self.__copy,
            bug_handler = RtfInvalidCodeException,
            run_level = self.__run_level,)
        # found destination means {\*\destination
        # if found, the RTF should be newer RTF
        found_destination = delete_info_obj.delete_info()
        self.__bracket_match('delete_data_info')

        # put picts in a separate file
        pict_obj = rtf2xml.pict.Pict(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            orig_file = self.__file, 
            out_file = self.__out_file,
            run_level = self.__run_level,
           )
        pict_obj.process_pict()
        self.__bracket_match('pict_data_info')

        correct_uni_obj = rtf2xml.correct_unicode.CorrectUnicode(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            run_level = self.__run_level,
            exception_handler = InvalidRtfException,
           )

        correct_uni_obj.correct_unicode()
        self.__bracket_match('correct_unicode_info')


        combine_obj = rtf2xml.combine_borders.CombineBorders(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,)
        combine_obj.combine_borders()
        self.__bracket_match('combine_borders_info')

        footnote_obj = rtf2xml.footnote.Footnote(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            )
        footnote_obj.separate_footnotes()
        self.__bracket_match('separate_footnotes_info')

        header_obj = rtf2xml.header.Header(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            )
        header_obj.separate_headers()
        self.__bracket_match('separate_headers_info')

        list_numbers_obj = rtf2xml.list_numbers.ListNumbers(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            )
        list_numbers_obj.fix_list_numbers()
        self.__bracket_match('list_number_info')

        preamble_div_obj = rtf2xml.preamble_div.PreambleDiv(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
             )
        list_of_lists = preamble_div_obj.make_preamble_divisions()
        self.__bracket_match('make_preamble_divisions')

        encode_obj = rtf2xml.default_encoding.DefaultEncoding(
            in_file = self.__temp_file,
            run_level = self.__run_level,
            bug_handler = RtfInvalidCodeException,
            )
        platform, code_page, default_font_num = encode_obj.find_default_encoding()

        hex2utf_obj = rtf2xml.hex_2_utf8.Hex2Utf8(
                in_file = self.__temp_file,
                copy = self.__copy, 
                area_to_convert = 'preamble', 
                char_file = self.__char_data, 
                default_char_map = code_page,
                run_level = self.__run_level,
                bug_handler = RtfInvalidCodeException,
                invalid_rtf_handler = InvalidRtfException,
                )  
        hex2utf_obj.convert_hex_2_utf8()
        self.__bracket_match('hex_2_utf_preamble')

        fonts_obj = rtf2xml.fonts.Fonts(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            default_font_num = default_font_num,
            run_level = self.__run_level,
            )
        special_font_dict = fonts_obj.convert_fonts()
        self.__bracket_match('fonts_info')

        color_obj = rtf2xml.colors.Colors(
            in_file = self.__temp_file,
            copy = self.__copy,
            bug_handler = RtfInvalidCodeException,
            run_level = self.__run_level,
            )
        color_obj.convert_colors()
        self.__bracket_match('colors_info')

        style_obj = rtf2xml.styles.Styles(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            )
        style_obj.convert_styles()
        self.__bracket_match('styles_info')

        info_obj = rtf2xml.info.Info(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,
            )
        info_obj.fix_info()

        default_font = special_font_dict.get('default-font')
        preamble_rest_obj = rtf2xml.preamble_rest.Preamble(
            file = self.__temp_file, copy = self.__copy,
            bug_handler = RtfInvalidCodeException,
            platform = platform, default_font = default_font,
            code_page = code_page)
        preamble_rest_obj.fix_preamble()
        self.__bracket_match('preamble_rest_info')

        old_rtf_obj = rtf2xml.old_rtf.OldRtf(
                in_file = self.__temp_file,
                bug_handler = RtfInvalidCodeException,
                run_level = self.__run_level,
                )
        # RTF can actually have destination groups and old RTF.
        # BAH!
        old_rtf = old_rtf_obj.check_if_old_rtf()
        if old_rtf:
            if self.__run_level > 5:
                msg = 'older RTF\n'
                msg += 'self.__run_level is "%s"\n' % self.__run_level 
                raise RtfInvalidCodeException, msg
                        
            if self.__run_level > 1:
                sys.stderr.write('File could be older RTF...\n')

            if found_destination:
                if self.__run_level > 1:
                    sys.stderr.write(
                        'File also has newer RTF.\n'
                        'Will do the best to convert.\n'
                    )
            add_brackets_obj = rtf2xml.add_brackets.AddBrackets(
                    in_file = self.__temp_file,
                    bug_handler = RtfInvalidCodeException,
                    copy = self.__copy,
                    run_level = self.__run_level,
                    )
            add_brackets_obj.add_brackets()

        fields_small_obj = rtf2xml.fields_small.FieldsSmall(
            in_file = self.__temp_file, 
            copy = self.__copy,
            bug_handler = RtfInvalidCodeException,
            run_level = self.__run_level,)
        fields_small_obj.fix_fields()
        self.__bracket_match('fix_small_fields_info')

        fields_large_obj = rtf2xml.fields_large.FieldsLarge(
            in_file = self.__temp_file, 
            copy = self.__copy, 
            bug_handler = RtfInvalidCodeException,
            run_level = self.__run_level)
        fields_large_obj.fix_fields()
        self.__bracket_match('fix_large_fields_info')

        sections_obj = rtf2xml.sections.Sections(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            run_level = self.__run_level,)
        sections_obj.make_sections()
        self.__bracket_match('sections_info')

        paragraphs_obj = rtf2xml.paragraphs.Paragraphs(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy,
            write_empty_para =  self.__empty_paragraphs,
            run_level = self.__run_level,)
        paragraphs_obj.make_paragraphs()
        self.__bracket_match('paragraphs_info')

        default_font = special_font_dict['default-font']
        paragraph_def_obj = rtf2xml.paragraph_def.ParagraphDef(
            in_file = self.__temp_file,
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            default_font = default_font,
            run_level = self.__run_level,)
        list_of_styles = paragraph_def_obj.make_paragraph_def()

        body_styles_obj = rtf2xml.body_styles.BodyStyles(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            list_of_styles = list_of_styles,
            run_level = self.__run_level,)
        body_styles_obj.insert_info()
        self.__bracket_match('body_styles_info')

        self.__bracket_match('paragraph_def_info')

        table_obj = rtf2xml.table.Table(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy,
                run_level = self.__run_level,)
        table_data = table_obj.make_table()
        self.__bracket_match('table_info')

        table_info_obj = rtf2xml.table_info.TableInfo(
            in_file = self.__temp_file, 
            bug_handler = RtfInvalidCodeException,
            copy = self.__copy, 
            table_data = table_data,
            run_level = self.__run_level,)
        table_info_obj.insert_info()
        self.__bracket_match('table__data_info')

        if self.__form_lists:
            make_list_obj =  rtf2xml.make_lists.MakeLists(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy, 
                headings_to_sections = self.__headings_to_sections,
                run_level = self.__run_level,
                list_of_lists = list_of_lists,
                )
            make_list_obj.make_lists()
            self.__bracket_match('form_lists_info')


        if self.__headings_to_sections:
            headings_to_sections_obj =  rtf2xml.headings_to_sections.HeadingsToSections(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy, 
                run_level = self.__run_level,)
            headings_to_sections_obj.make_sections()
            self.__bracket_match('headings_to_sections_info')

        if self.__group_styles:
            group_styles_obj = rtf2xml.group_styles.GroupStyles(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy, 
                wrap = 1,
                run_level = self.__run_level,)
            group_styles_obj.group_styles()
            self.__bracket_match('group_styles_info')
        if self.__group_borders:
            group_borders_obj = rtf2xml.group_borders.GroupBorders(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy, 
                wrap = 1,
                run_level = self.__run_level,)
            group_borders_obj.group_borders()
            self.__bracket_match('group_borders_info')


        inline_obj = rtf2xml.inline.Inline(
                in_file = self.__temp_file, 
                bug_handler = RtfInvalidCodeException,
                copy = self.__copy,
                run_level = self.__run_level,)
        inline_obj.form_tags()
        self.__bracket_match('inline_info')



        hex2utf_obj.update_values(file = self.__temp_file,
                            area_to_convert = 'body',
                            copy = self.__copy,
                            char_file = self.__char_data,
                            convert_caps = self.__convert_caps, 
                            convert_symbol = self.__convert_symbol,
                            convert_wingdings = self.__convert_wingdings,
                            convert_zapf = self.__convert_zapf,
                            symbol = 1,
                            wingdings = 1,
                            dingbats = 1,
                )
        hex2utf_obj.convert_hex_2_utf8()

        header_obj.join_headers()

        footnote_obj.join_footnotes()

        tags_obj = rtf2xml.convert_to_tags.ConvertToTags(
                in_file = self.__temp_file,
                copy = self.__copy, 
                dtd_path = self.__dtd_path,
                indent = self.__indent,
                run_level = self.__run_level,
                no_dtd = self.__no_dtd,
                bug_handler = RtfInvalidCodeException,
                )

        tags_obj.convert_to_tags()



        output_obj = rtf2xml.output.Output(
                file = self.__temp_file, 
                orig_file = self.__file,
                output_dir = self.__out_dir,
                out_file = self.__out_file,
            )
        output_obj.output()
        os.remove(self.__temp_file)
        return self.__exit_level


    def __bracket_match(self, file_name):
        if self.__run_level > 2:
            good_br, msg =  self.__check_brack_obj.check_brackets()
            if good_br:
                pass
               # sys.stderr.write( msg + ' in ' + file_name + "\n")
            else:
               msg += msg +  " in file '" + file_name + "'\n" 
               raise RtfInvalidCodeException, msg

    def __return_code(self, num):
        if num == None:
            return
        if int(num) > self.__exit_level:
            self.__exit_level = num
        
    def __make_temp_file(self,file):
        """Make a temporary file to parse"""
	write_file="rtf_write_file"
	read_obj = open(file,'r')
	write_obj = open(write_file, 'w')
	line = "dummy"
	while line:
		line = read_obj.read(1000)
		write_obj.write(line )
	read_obj.close()
	write_obj.close()
        return write_file

    """
mi<tg<open______<style-sheet\n
mi<tg<close_____<style-sheet\n
mi<tg<open-att__<footnote<num>1\n
mi<tg<empty-att_<page-definition<margin>33\n
mi<tg<empty_____<para\n
"""
