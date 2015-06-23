#!/usr/bin/env python

import sys
import os

class inputs:
    def check_next_argvi(self):
        self.argi += 1
        if self.argi == self.argc:
            print "Missing argument after flag: " + self.argv[self.argi-1]
            print_usage()
            sys.exit()
                
    def choose_suffix(self):
        if   ".rgvcf" in self.infile_name: 
            self.filetype = self.RGVCF
            self.outfile_name = self.infile_name.replace(".rgvcf", ".seg")
        elif  ".gvcf" in self.infile_name: 
            self.filetype = self.GVCF
            self.outfile_name = self.infile_name.replace(".gvcf", ".seg")
        elif   ".vcf" in self.infile_name: 
            self.filetype = self.VCF
            self.outfile_name = self.infile_name.replace(".vcf", ".seg")
        else: print "File type can not be determined, suffix ends with '.vcf', '.gvcf' or '.rgvcf'."
        #print self.outfile_name, self.filetype # DEBUG
                
    def __init__(self, argv):
        [self.VCF, self.GVCF, self.RGVCF] = range ( 3 ) # enum vcf, gvcf rgvcf 
        self.argv = argv
        self.argc = len( self.argv )
        self.argi = 1
        while ( self.argi < self.argc ):
            if self.argv[self.argi] == "-i":
                self.check_next_argvi()
                self.infile_name = self.argv[ self.argi ]
                if not (os.path.isfile( self.infile_name) and os.access( self.infile_name, os.R_OK ) ):
                    print "Invalid file: ", self.infile_name
                    print_usage()
                else:
                    self.choose_suffix();
            elif self.argv[self.argi] == "-seqlen":
                self.check_next_argvi()
                self.seqlen = int( self.argv[self.argi] )
            else:
                print "Invalid flag: ", self.argv[self.argi] 
                print_usage()
                sys.exit()
            self.argi += 1


class something2seg:
    def __init__(self, infile_type, infile_name, outfile_name, seqlen):
        self.infile_type = infile_type
        self.outfile_name = outfile_name
        self.seqlen = seqlen
        [self.VCF, self.GVCF, self.RGVCF] = range ( 3 ) # enum vcf, gvcf rgvcf 
        self.infile = open ( infile_name, 'r' )
        self.infile_Lines = self.infile.readlines()
        self.infile.close()
        self.variant_pos = 1
	self.variant=""
        self.genetic_break = "F"
	self.cursor = 1
	self.seg_start = 1
	self.seg_state = "T"
	self.seg_end = 1
	self.next_position = 1
	self.chrom = ""
	self.debug_break = False

#####################

    #def find_next_position(self):
	#if self.infile_type == self.VCF:
	    #self.next_position = int( self.infile_Lines [self.line_index + 1].split("\t")[1] ) if self.line_index + 1 < self.infile_size else self.seqlen
        #elif ( self.infile_type == self.GVCF ):
	    ##
	    #nextLineIndex = self.line_index + 1
	    #while ( self.infile_Lines [nextLineIndex].split("\t")[6] == "REFCALL"):
		#nextLineIndex += 1
	    #self.line_index = nextLineIndex-1

	    #print ("now at line: \n ", self.infile_Lines [self.line_index ])
	    #line_split = self.infile_Lines [self.line_index ].split("\t")
	    #self.next_position = int( line_split[1] ) if self.line_index + 1 < self.infile_size else self.seqlen
            #field = line_split[7]
            #END_index = field.find ("END=")
            #field = field.strip(field[0:END_index]).strip("END=")
            #semi_col_index = field.find (";")
            #self.seg_end = int(field[0:semi_col_index])

#######################

    def core(self):
        self.pre_process();
        self.outfile = open ( self.outfile_name, 'w' )         
        self.infile_size = len ( self.infile_Lines )
        #print self.line_index, infile_size  # DEBUG

        line_split = self.line.strip().split("\t")
        self.chrom = line_split [0] 

        # define what missing vairant should look like, just number of .s
        self.missingvariant = ""
        for field in range( 9, len(line_split)):                        
            self.missingvariant += ".."
        # Initialize the first line of vcf file, start from position 1            
        #if self.infile_type != self.VCF:
            #self.line_index -= 1
            #self.find_next_position ()
            #self.line_index += 1
            #self.seg_len = self.next_position - self.variant_pos
            #self.seg_status = "T"
            #current_line = `self.variant_pos` + "\t" + \
                           #`self.seg_len`     + "\t" + \
                           #self.seg_status    + "\t" + \
                           #self.genetic_break + "\t" + \
                           #self.chrom         + "\t" + \
                           #self.missingvariant + "\n"
        
            #self.outfile.write ( current_line )
        while self.line_index < self.infile_size:
	    # 1. start a seg,
	    # 2. find the end position of this seg ( currentLine )
		# extract the end position, and information at the seg
		# write
	    # 3. check for the next line of the currentLine, if the next position is not consective,
	    # write missing data entry, otherwise, repeat 1

	    #old:
	    #self.extract_infile_line ( self.infile_Lines [self.line_index] )
	    #self.find_next_position()
            #self.write_seg_line()
            #self.line_index += 2

	    #new:
	    if self.debug_break:
		break
	    self.extract_start_info()
	    if self.debug_break:
		break
	    self.extract_end_info()
	    if self.debug_break:
		break
	    self.write_seg_file()
	    if self.debug_break:
		break
	    
	    #debugging:
	    #if self.genetic_break == "T":
		#break
	    #if self.line_index > 200:
		#break
            #pass

        self.outfile.close()




    def extract_start_info( self ):

	if self.genetic_break == "F":
	    self.line_index+=1
	if self.line_index >= self.infile_size:
		    #for now don't think about writing last line of file, just get out
		    self.debug_break = True
		    return
	lineposition = int(self.infile_Lines[self.line_index].split("\t")[1])
	self.seg_start = min( self.cursor+1, lineposition )
	if self.genetic_break == "T":
	    print("for extract_start_info after genetic break, lineposition is")
	    print(`lineposition`)
	    print("cursor is at")
	    print(`self.cursor`)
	# if the line position is greater than cursor+1, we have missing data in the segment
	self.seg_state = "F" if ( lineposition > self.cursor+1) else "T"


    def extract_end_info( self ):
	while ( True ):

	    if self.line_index == self.infile_size:
		    #for now don't think about writing last line of file, just get out
		    self.debug_break = True
		    break

	    currentLineSplit = self.infile_Lines[self.line_index].split("\t")

	    if currentLineSplit[0] == self.chrom:
		self.genetic_break = "F"
		if ( currentLineSplit[6].find("REFCALL") >= 0 ):
		    # for a refcall line we need to move the cursor to END
		    self.seg_state="T"
		    field = currentLineSplit[7]
		    END_index = field.find ("END=")
		    field = field.strip(field[0:END_index]).strip("END=")
		    semi_col_index = field.find (";")
		    self.cursor = int(field[0:semi_col_index])
		else:
		    lineposition = int(currentLineSplit[1])
		    #assign the variant to '01' or '..' as apropriate
		    self.variant=""
		    for sample in range( 9, len(currentLineSplit) ):
			current_sample = currentLineSplit[sample]
			assert(self.infile_type == self.GVCF)
			self.variant += current_sample[0] if ( current_sample[0] == "." or current_sample[0] == "0") else `1`
			self.variant += current_sample[2] if ( current_sample[2] == "." or current_sample[2] == "0") else `1`
		    self.cursor = lineposition
		    self.seg_end = self.cursor
		    break
		self.line_index += 1
		if self.line_index == self.infile_size:
		    #for now don't think about writing last line of file if REFCALL, just get out
		    self.debug_break = True
		    break

	    else:      # need to extract info for last line for the chromosome
		# current line is last line of chromosome
		currentLineSplit = self.infile_Lines[self.line_index-1].split("\t")
		self.genetic_break = "T"

		if ( currentLineSplit[6].find("REFCALL") >= 0 ):
		    # for a refcall line we need to move the cursor to END
		    #self.seg_state="T"
		    #field = currentLineSplit[7]
		    #END_index = field.find ("END=")
		    #field = field.strip(field[0:END_index]).strip("END=")
		    #semi_col_index = field.find (";")
		    #self.cursor = int(field[0:semi_col_index])
		    #self.variant=""
		    for sample in range( 9, len(currentLineSplit) ):
			current_sample = currentLineSplit[sample]
			assert(self.infile_type == self.GVCF)
			self.variant += "0"  # this is a hack, not sure how to deal with REFCALL stating . for 0
			self.variant += "0"
			#self.variant += current_sample[0] if ( current_sample[0] == "." or current_sample[0] == "0") else `1`
			#self.variant += current_sample[2] if ( current_sample[2] == "." or current_sample[2] == "0") else `1`
		    self.seg_end = self.cursor
		    print("in genetic break REFCALL")
		    print("seg end is")
		    print(`self.seg_end`)
		    print("")
		    break
		else:
		    lineposition = int(currentLineSplit[1])
		    #assign the variant to '01' or '..' as apropriate
		    self.variant=""
		    for sample in range( 9, len(currentLineSplit) ):
			current_sample = currentLineSplit[sample]
			assert(self.infile_type == self.GVCF)
			self.variant += current_sample[0] if ( current_sample[0] == "." or current_sample[0] == "0") else `1`
			self.variant += current_sample[2] if ( current_sample[2] == "." or current_sample[2] == "0") else `1`
		    self.cursor = lineposition
		    self.seg_end = self.cursor
		    print("in genetic break non-REFCALL")
		    print("seg end is")
		    print(`self.seg_end`)
		    print("variant is")
		    print(`self.variant`)
		    print("")
		    break


		# extract info
		    # could be REFCALL which would cause problems in write_seg_file...
		# need a way to pass self.genetic_break = "T" to the next line...
		# for now putting "T" in last line of chromosome

    def write_seg_file( self ):
	currentLineSplit = self.infile_Lines[self.line_index].split("\t")
	if self.genetic_break == "F":
	    if (currentLineSplit[6].find("badReads") >= 0 ):
		#write missing line, segment ends in missing, segment may or may not be invariant
		self.seg_len = self.seg_end - self.seg_start + 1
		missing_line = `self.seg_end` + "\t" + \
			       `self.seg_len`     + "\t" + \
			       self.seg_state    + "\t" + \
			       self.genetic_break + "\t" + \
			       self.chrom         + "\t" + \
			       self.variant + "\n"

		self.outfile.write ( missing_line )
		self.variant = ""
	    elif (currentLineSplit[6].find("PASS") >=0 ):
		#write variant line, segment ends in variant, segment may or may not be invariant
		self.seg_len = self.seg_end - self.seg_start + 1
		variant_line = `self.seg_end` + "\t" + \
			       `self.seg_len`     + "\t" + \
			       self.seg_state    + "\t" + \
			       self.genetic_break + "\t" + \
			       self.chrom         + "\t" + \
			       self.variant + "\n"
		self.outfile.write( variant_line )
		#reset variant for next segment
		self.variant = ""
	    # for debugging
	    #if self.chrom == "flattened_line_12":
		#self.debug_break = True
	else: # writing the last line of earlier chromsome
	    #if REFCALL:
	    self.seg_len = self.seg_end - self.seg_start + 1
	    variant_line = `self.seg_end` + "\t" + \
			   `self.seg_len`     + "\t" + \
			   self.seg_state    + "\t" + \
			   self.genetic_break + "\t" + \
			   self.chrom         + "\t" + \
			   self.variant + "\n"
	    self.outfile.write( variant_line )
	    #reset variant for next segment
	    self.variant = ""

	    # setup for next chromosome
	    self.chrom = self.infile_Lines[self.line_index+1].split("\t")[0]



	    #need to consider different cases, just looking at REFCALL for now






    def pre_process ( self ):
        # Pre-process, skip all the comments lines,
        # Extract the number of taxa ( 2*number_of_sample ) at the last line
        for self.line_index, self.line in enumerate( self.infile_Lines ):
            if self.line.find ( "##" ) == 0: # skipping the comments
                continue
            elif self.line.find ( "#" ) == 0: #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  NA00001 NA00002 NA00003
                line_split = self.line.strip().split("\t")
                self.taxa = 2 * ( len(line_split) - 9 ) # where ( len(line_split) - 9 ) computes the number of the samples
            else:
                break; # stops at the first line
        #print "number of sample is ",self.taxa # DEBUG

############################

    #def extract_infile_line( self, line ):
        #line_split = line.strip().split("\t")
        #self.chrom = line_split [0]
        #self.variant_pos = int(line_split [1])

        #self.variant_entry = ( line_split[6].find("REFCALL") < 0 )
        #if self.variant_entry:
            #self.seg_end = self.variant_pos
        ##else:
            ##field = line_split[7]
            ##END_index = field.find ("END=")
            ##field = field.strip(field[0:END_index]).strip("END=")
            ##semi_col_index = field.find (";")
            ##self.seg_end = int(field[0:semi_col_index])

        #self.variant = ""
	#print ( "Extracting from line: ", line)
        #for field in range( 9, len(line_split) ):
            #current_field = line_split[field]
	    #if (line_split[6].find("REFCALL") >= 0):
		#assert( self.infile_type == self.GVCF )
		#self.variant += "00"
	    #elif ( line_split[6].find("PASS") >= 0 ):
		#assert(self.infile_type == self.GVCF)
		#self.variant += current_field[0] if ( current_field[0] == "." or current_field[0] == "0") else `1`
		#self.variant += current_field[2] if ( current_field[2] == "." or current_field[2] == "0") else `1`
	    #else:
		#assert(self.infile_type == self.GVCF)
		#self.variant += ".."
## GVCF, if we find refcall in line, self.variant += 0

        
    #def write_seg_line (self):
        
        #if ( self.infile_type == self.VCF ):
            ## for vcf file, no missing data is represented. Sequence segment between two variants reads are treated as Invariant.
            #self.seg_len = self.next_position - self.variant_pos
            #self.seg_status = "T"
            #variant_line = `self.variant_pos` + "\t" + \
                           #`self.seg_len`     + "\t" + \
                           #"T" + "\t" + self.genetic_break + "\t" + self.chrom + "\t" + self.variant + "\n"
            #self.outfile.write ( variant_line )
        #elif self.infile_type == self.GVCF:
            #self.seg_len = self.seg_end - self.variant_pos + 1
            #invariant_line = `self.variant_pos` + "\t" + \
                             #`self.seg_len`     + "\t" + \
                             #"T" + "\t" + self.genetic_break + "\t" + self.chrom + "\t" + self.variant + "\n"
            #self.outfile.write ( invariant_line ) #this could be '00' is refcall followed by missing

            #self.seg_len = self.next_position - self.seg_end
            #missing_line = `self.variant_pos` + "\t" + \
                           #`self.seg_len`     + "\t" + \
                           #"F" + "\t" + self.genetic_break + "\t" + self.chrom + "\t" + self.missingvariant + "\n"
            #if self.seg_len > 1:
                #self.outfile.write ( missing_line )
        #elif self.infile_type == self.RGVCF:
            #self.seg_len = self.seg_end - self.variant_pos + 1
            #missing_line = `self.variant_pos` + "\t" + \
                           #`self.seg_len`     + "\t" + \
                           #"F" + "\t" + self.genetic_break + "\t" + self.chrom + "\t" + self.missingvariant + "\n"
            #self.outfile.write ( missing_line )
            #self.seg_len = self.next_position - self.seg_end
            #invariant_line = `self.variant_pos` + "\t" + \
                             #`self.seg_len`     + "\t" + \
                             #"T" + "\t" + self.genetic_break + "\t" + self.chrom + "\t" + self.missingvariant + "\n"
            #if self.seg_len > 1:
                #self.outfile.write ( invariant_line )
        #else:
            #print "ERROR"
            #sys.exit()

##########################
                            
def print_usage():
    print "USAGE:"
    print "    ./vcf2seg -i FILENAME -seqlen INT"
    sys.exit()


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print_usage()
    elif sys.argv[1] == "-help":
        print_usage()
    
    myinput = inputs( sys.argv )
    myprocess = something2seg(myinput.filetype, myinput.infile_name, myinput.outfile_name, myinput.seqlen)
    myprocess.core()
