# Time-stamp: <2011-01-20 18:21:42 Jake Biesinger>

"""Description:

Copyright (c) 2008,2009,2010 Yong Zhang, Tao Liu <taoliu@jimmy.harvard.edu>

This code is free software; you can redistribute it and/or modify it
under the terms of the Artistic License (see the file COPYING included
with the distribution).

@status: beta
@version: $Revision$
@originalauthor:  Yong Zhang, Tao Liu
@originalcontact: taoliu@jimmy.harvard.edu

Modifications to probabilistically align reads to regions with highest
enrichment performed by Jacob Biesinger. Repackaged as "AREM" in accordance
with copyright restrictions.

@author: Biesinger, W Jacob B
@contact: jake.biesinger@gmail.com


Changes to this file since original release of MACS 1.4 (summer wishes):
  December/January 2011
    * Updated names (AREM, not MACS14)
    * Modified sort/storage to include multi-reads
    
"""

# ------------------------------------
# python modules
# ------------------------------------
import re
import sys
import logging
import struct
from array import array
from random import sample as random_sample
from operator import itemgetter
from itertools import izip as itertools_izip
from AREM.Constants import *

# ------------------------------------
# constants
# ------------------------------------
__version__ = "FeatIO $Revision$"
__author__ = "Tao Liu <taoliu@jimmy.harvard.edu>"
__doc__ = "PeakIO, FWTrackI, TrackI, WigTrackI and BinKeeperI classes"

# ------------------------------------
# Misc functions
# ------------------------------------


# ------------------------------------
# Classes
# ------------------------------------

class PeakIO:
    """IO for peak information.

    """
    def __init__ (self):
        self.peaks = {}
    
    def add (self, chromosome, start, end, summit=None, 
             peak_height=None, number_tags=None, 
             pvalue=None, fold_enrichment=None, fdr=None):
        """items: (peak start,peak end, peak length, peak summit, peak
        height, number of tags in peak region, peak pvalue, peak
        fold_enrichment, fdr) <-- tuple type
        """
        if not self.peaks.has_key(chromosome):
            self.peaks[chromosome]=[]
        self.peaks[chromosome].append((start,end,end-start,summit,
                                       peak_height,number_tags,
                                       pvalue,fold_enrichment,fdr))

    def filter_pvalue (self, pvalue_cut ):
        peaks = self.peaks
        new_peaks = {}
        chrs = peaks.keys()
        chrs.sort()
        for chrom in chrs:
            new_peaks[chrom]=[p for p in peaks[chrom] if p[6] >= pvalue_cut]
        self.peaks = new_peaks

    def filter_fc (self, fc_low, fc_up=None ):
        """Filter peaks in a given fc range.

        If fc_low and fc_up is assigned, the peaks with fc in [fc_low,fc_up)
        
        """
        peaks = self.peaks
        new_peaks = {}
        chrs = peaks.keys()
        chrs.sort()
        if fc_up:
            for chrom in chrs:
                new_peaks[chrom]=[p for p in peaks[chrom] if p[7] >= fc_low and p[7]<fc_up]
        else:
            for chrom in chrs:
                new_peaks[chrom]=[p for p in peaks[chrom] if p[7] >= fc_low]
        self.peaks = new_peaks

    def total (self):
        peaks = self.peaks
        chrs = peaks.keys()
        chrs.sort()
        x = 0
        for chrom in chrs:
            x += len(peaks[chrom])
        return x
    
    def ave_fold_enrichment (self):
        peaks = self.peaks
        chrs = peaks.keys()
        chrs.sort()
        x = 0
        t = 0
        for chrom in chrs:
            x += len(peaks[chrom])
            for p in peaks[chrom]:
                t+=p[7]
        return t/x

    def max_fold_enrichment (self):
        """Return the maximum fc.
        
        """
        peaks = self.peaks
        chrs = peaks.keys()
        chrs.sort()
        x = 0
        for chrom in chrs:
            if peaks[chrom]:
                m = max([i[7] for i in peaks[chrom]])
                if m>x:
                    x=m
        return x
        
    
    def tobed (self):
        text = ""
        chrs = self.peaks.keys()
        chrs.sort()
        for chrom in chrs:
            for peak in self.peaks[chrom]:
                text+= "%s\t%d\t%d\n" % (chrom,peak[0],peak[1])
        return text

    def towig (self):
        text = ""
        chrs = self.peaks.keys()
        chrs.sort()
        for chrom in chrs:
            for peak in self.peaks[chrom]:
                text+= "%s\t%d\t%d\n" % (peak[0],peak[1])
        return text
        
    def init_from_dict (self, data):
        """Initialize the data from a dictionary. Improper assignment
        will damage the data structure.
        
        """
        self.peaks = {}
        chrs = data.keys()
        chrs.sort()
        for chrom in chrs:
            self.peaks[chrom]=[]
            a = self.peaks[chrom].append
            for i in data[chrom]:
                a(i)

    def merge_overlap ( self ):
        """peak_candidates[chrom] = [(peak_start,peak_end,peak_length,peak_summit,peak_height,number_cpr_tags)...]

        """
        peaks = self.peaks
        new_peaks = {}
        chrs = peaks.keys()
        chrs.sort()
        for chrom in chrs:
            new_peaks[chrom]=[]
            n_append = new_peaks[chrom].append
            prev_peak = None
            peaks_chr = peaks[chrom]
            for i in xrange(len(peaks_chr)):
                if not prev_peak:
                    prev_peak = peaks_chr[i]
                    continue
                else:
                    if peaks_chr[i][0] <= prev_peak[1]:
                        s_new_peak = prev_peak[0]
                        e_new_peak = peaks_chr[i][1]
                        l_new_peak = e_new_peak-s_new_peak
                        if peaks_chr[i][4] > prev_peak[4]:
                            summit_new_peak = peaks_chr[i][3]
                            h_new_peak = peaks_chr[i][4]
                        else:
                            summit_new_peak = prev_peak[3]
                            h_new_peak = prev_peak[4]
                        prev_peak = (s_new_peak,e_new_peak,l_new_peak,summit_new_peak,h_new_peak,peaks_chr[i][5]+prev_peak[5])
                    else:
                        n_append(prev_peak)
                        prev_peak = peaks_chr[i]
            if prev_peak:
                n_append(prev_peak)
        del peaks
        self.peaks = new_peaks
        return True

    def overlap_with_other_peaks (self, peaks2, cover=0):
        """Peaks2 is a PeakIO object or dictionary with can be
        initialzed as a PeakIO. check __init__ for PeakIO for detail.

        return how many peaks are intersected by peaks2 by percentage
        coverage on peaks2(if 50%, cover = 0.5).
        """
        peaks1 = self.peaks
        if isinstance(peaks2,PeakIO):
            peaks2 = peaks2.peaks
        total_num = 0
        chrs1 = peaks1.keys()
        chrs2 = peaks2.keys()
        for k in chrs1:
            if not chrs2.count(k):
                continue
            rl1_k = iter(peaks1[k])
            rl2_k = iter(peaks2[k])
            tmp_n = False
            try:
                r1 = rl1_k.next()
                r2 = rl2_k.next()
                while (True):
                    if r2[0] < r1[1] and r1[0] < r2[1]:
                        a = sorted([r1[0],r1[1],r2[0],r2[1]])
                        if float(a[2]-a[1]+1)/r2[2] > cover:
                            if not tmp_n:
                                total_num+=1
                                tmp_n = True
                    if r1[1] < r2[1]:
                        r1 = rl1_k.next()
                        tmp_n = False
                    else:
                        r2 = rl2_k.next()
            except StopIteration:
                continue
        return total_num
        

class FWTrackII:
    """Fixed Width Locations Track class II along the whole genome
    (commonly with the same annotation type), which are stored in a
    dict.

    Locations are stored and organized by sequence names (chr names) in a
    dict. They can be sorted by calling self.sort() function.
    
    multireads are stored as (start, index) rather than just start
    """
    def __init__ (self,fw=0,anno=""):
        """fw is the fixed-width for all locations.
        
        """
        self.fw = fw
        self._locations = {}           # locations
        self._indexes = {}             # index into multi read arrays
        self._sorted = False
        self.total = 0                  # total tags
        self.annotation = anno   # need to be figured out
        self.prob_aligns = array(FBYTE4, [1])
        self.prior_aligns = array(FBYTE4, [1])  # prior prob of aligning- based on quals
        self.enrich_scores = array(FBYTE4, [1])
        self.group_starts = array(BYTE4, [])
        self.total_multi = 0
        self._togetherplus = None
        self._togetherminus = None

    def add_loc (self, chromosome, fiveendpos, strand, index=0):
        """Add a location to the list according to the sequence name.
        
        chromosome -- mostly the chromosome name
        fiveendpos -- 5' end pos, left for plus strand, right for neg strand
        strand     -- 0: plus, 1: minus
        index      -- index for multi-reads, left for plus strand, right for neg strand
        """
        if not self._locations.has_key(chromosome):
            self._locations[chromosome] = [array(BYTE4,[]),array(BYTE4,[])] # for (+strand, -strand)
            self._indexes[chromosome] = [array(BYTE4,[]),array(BYTE4,[])] # for (+strand, -strand)
        self._locations[chromosome][strand].append(fiveendpos)
        self._indexes[chromosome][strand].append(index)
    
    def get_locations_by_chr (self, chromosome):
        """Return a tuple of two lists of locations for certain chromosome.

        """
        if self._locations.has_key(chromosome):
            return self._locations[chromosome]
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_indexes_by_chr (self, chromosome):
        """Return a tuple of two lists of indexes for a certain chromosome.

        """
        if self._indexes.has_key(chromosome):
            return self._indexes[chromosome]
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))
    
    def get_locations_indexes_by_chr(self, chromosome):
        """Return a tuple of (location, index), parsed from the normal large array
        
        """
        if self._locations.has_key(chromosome):
            return (zip(self._locations[chromosome][0],self._indexes[chromosome][0]),
                    zip(self._locations[chromosome][1],self._indexes[chromosome][1]))
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_chr_names (self):
        """Return all the chromosome names stored in this track object.
        """
        l = self._locations.keys()
        l.sort()
        return l

    def length (self):
        """Total sequenced length = total number of tags * width of tag		
        """
        return self.total*self.fw

    def sort (self):
        """Naive sorting for locations.
        
        """
        for k in self._locations.keys():
            self.sort_chrom(k)
        self._sorted = True
    
    def argsort(self, seq):
        """return the positions in seq that would give a sorted list
        """
        return sorted(range(len(seq)), key=seq.__getitem__)

    def sort_chrom(self, k):
        """Sort the start locations for the chromosome, keeping the indexes together
        """
        # argsort
        locs = self._locations[k][0]
        indexes = self._indexes[k][0]
        sort_order = self.argsort(locs)
        self._locations[k][0] = array('i', (locs[i] for i in sort_order))
        self._indexes[k][0] = array('i', (indexes[i] for i in sort_order))
        
        locs = self._locations[k][1]
        indexes = self._indexes[k][1]
        sort_order = self.argsort(locs)
        self._locations[k][1] = array('i', (locs[i] for i in sort_order))
        self._indexes[k][1] = array('i', (indexes[i] for i in sort_order))
        
        ## zip, sort, unzip -- Jake - this method is MUCH slower
        ## zip location, index; then sort the tuple by location, then unzip back into place
        #g0 = itemgetter(0)
        #(tmparrayplus,tmparrayminus) = self.get_locations_indexes_by_chr(k)
        #tmparrayplus.sort(key=g0)
        #self._locations[k][0], self._indexes[k][0] = map(list, zip(*tmparrayplus))
        #tmparrayminus.sort(key=g0)
        #self._locations[k][1], self._indexes[k][1] = map(list, zip(*tmparrayminus))

    def filter_dup (self,maxnum):
        """Filter the duplicated reads.

        Run it right after you add all data into this object.
        """
        if not self._sorted:
            self.sort()
        self.total = 0
        for k in self._locations.keys(): # for each chromosome
            # + strand
            plus = self._locations[k][0]
            plus_ind = self._indexes[k][0]
            total_unique = 0
            if len(plus) < 1:
                new_plus = array(BYTE4,[])
                new_plus_ind = array(BYTE4,[])
            else:
                new_plus = array(BYTE4,[plus[0]])
                new_plus_ind = array(BYTE4,[plus_ind[0]])
                pappend = new_plus.append
                pind_append = new_plus_ind.append
                n = 1                # the number of tags in the current location
                current_loc = plus[0]
                for ind, p in itertools_izip(plus_ind[1:], plus[1:]):
                    if p == current_loc:
                        n += 1
                        if n <= maxnum:
                            pappend(p)
                            pind_append(ind)
                            if ind == 0:
                                total_unique += 1
                    else:
                        current_loc = p
                        pappend(p)
                        pind_append(ind)
                        if ind == 0:
                            total_unique += 1
                        n = 1
                self.total +=  total_unique

            # - strand
            minus = self._locations[k][1]
            minus_ind = self._indexes[k][1]
            total_unique = 0
            if len(minus) < 1:
                new_minus = array(BYTE4,[])
                new_minus_ind = array(BYTE4,[])
            else:
                new_minus = array(BYTE4,[minus[0]])
                new_minus_ind = array(BYTE4,[minus_ind[0]])
                mappend = new_minus.append
                mind_append = new_minus_ind.append
                n = 1                # the number of tags in the current location
                current_loc = minus[0]
                for ind, m in itertools_izip(minus_ind[1:], minus[1:]):
                    if m == current_loc:
                        n += 1
                        if n <= maxnum:
                            mappend(m)
                            mind_append(ind)
                            if ind == 0:
                                total_unique += 1
                    else:
                        current_loc = m
                        mappend(m)
                        mind_append(ind)
                        if ind == 0:
                            total_unique += 1
                        n = 1
                self.total +=  total_unique
            self._locations[k]=[new_plus,new_minus]
            self._indexes[k] = [new_plus_ind, new_minus_ind]

    def merge_plus_minus_locations_naive (self):
        """Merge plus and minus strand locations
        
        """
        for chrom in self._locations.keys():
            self._locations[chrom][0].extend(self._locations[chrom][1])
            self._indexes[chrom][0].extend(self._indexes[chrom][1])
            self._locations[chrom][1] = []
            self._indexes[chrom][1] = []
            self.sort_chrom(chrom)

    def sample (self, percent):
        """Sample the tags for a given percentage.

        Warning: the current object is changed!
        """
        self.total = 0
        for key in self._locations.keys():
            plus = self._locations[key][0]
            plus_ind = self._indexes[key][0]
            total_plus = len(plus)
            num = int(total_plus*percent)
            ind_tokeep = sorted(random_sample(xrange(total_plus), num))
            self._locations[key][0] = array(BYTE4, (plus[i] for i in ind_tokeep))
            total_unique = 0
            self._indexes[key][0] = array(BYTE4, [])
            pappend = self._indexes[key][0].append
            for i in ind_tokeep:
                pappend(plus_ind[i])
                if plus_ind[i] == 0:
                    total_unique += 1
            
            minus = self._locations[key][1]
            minus_ind = self._indexes[key][1]
            total_minus = len(minus)
            num = int(total_minus*percent)
            ind_tokeep = sorted(random_sample(xrange(total_minus), num))
            self._locations[key][1] = array(BYTE4, (minus[i] for i in ind_tokeep))
            self._indexes[key][1] = array(BYTE4, [])
            mappend = self._indexes[key][1].append
            for i in ind_tokeep:
                mappend(minus_ind[i])
                if minus_ind[i] == 0:
                    total_unique += 1

            self.total += total_unique
            
    def __str__ (self):
        return self._to_wiggle()
        
    def _to_wiggle (self):
        """Use a lot of memory!  
        
        # Jake- I don't think this works for redundant tags
        
        """
        t = "track type=wiggle_0 name=\"tag list\" description=\"%s\"\n" % (self.annotation)
        for k in self._locations.keys():
            if self._locations[k][0]:
                t += "variableStep chrom=%s span=%d strand=0\n" % (k,self.fw)
                for i in self._locations[k][0]:
                    t += "%d\t1\n" % i
            if self._locations[k][1]:
                t += "variableStep chrom=%s span=%d strand=1\n" % (k,self.fw)
                for i in self._locations[k][1]:
                    t += "%d\t1\n" % i
        return t

class FWTrackI:
    """Fixed Width Ranges along the whole genome (commonly with the
    same annotation type), which are stored in a dict.

    Locations are stored and organized by sequence names (chr names) in a
    dict. They can be sorted by calling self.sort() function.

    Example:
       >>> tabfile = TabFile('tag.bed',format='bed',mode='r')
       >>> track = FWTrackI()
       >>> for (chromosome,rg) in tabfile:
       ...    track.add_location(chromosome,rg)
       >>> track.get_locations_by_chr['chr1'] # all locations in chr1 
    """
    def __init__ (self,fw=0,anno=""):
        """fw is the fixed-width for all locations
        """
        self.fw = fw
        self._locations = {}           # locations
        self._counts = {}              # number of tags at the same location
        self._well_merged = False
        self.total = 0					# total tags
        self.total_unique = 0		# total unique tags
        self.annotation = anno   # need to be figured out

    def add_loc (self, chromosome, fiveendpos, strand):
        """Add a location to the list according to the sequence name.
        
        chromosome -- mostly the chromosome name
        fiveendpos -- 5' end pos, left for plus strand, neg for neg strand
        strand     -- 0: plus, 1: minus
        """
        if not self._locations.has_key(chromosome):
            self._locations[chromosome] = [array(BYTE4,[]),array(BYTE4,[])] # for (+strand, -strand)
            self._counts[chromosome] = [array(UBYTE2,[]),array(UBYTE2,[])] # for (+,-)
        self._locations[chromosome][strand].append(fiveendpos)
        self._counts[chromosome][strand].append(1)
        self.total+=1

    def get_locations_by_chr (self, chromosome):
        """Return a tuple of two lists of locations for certain chromosome.

        """
        if self._locations.has_key(chromosome):
            return self._locations[chromosome]
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_counts_by_chr (self, chromosome):
        """Return a tuple of two lists of counts for certain chromosome.

        """
        if self._counts.has_key(chromosome):
            return self._counts[chromosome]
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_loc_counts_by_chr (self, chromosome):
        """Return a tuple of two lists of (loc,count) for certain chromosome.

        """
        if self._counts.has_key(chromosome):
            return (zip(self._locations[chromosome][0],self._counts[chromosome][0]),
                    zip(self._locations[chromosome][1],self._counts[chromosome][1]))
        else:
            raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_chr_names (self):
        """Return all the chromosome names stored in this track object.
        """
        l = self._locations.keys()
        l.sort()
        return l

    def length (self):
        """Total sequenced length = total number of tags * width of tag		
        """
        return self.total*self.fw

    def sort (self):
        """Naive sorting for locations.
        
        """
        for k in self._locations.keys():
            g0 = itemgetter(0)
            (tmparrayplus,tmparrayminus) = self.get_loc_counts_by_chr(k)
            tmparrayplus.sort(key=g0)
            self._locations[k][0], self._counts[k][0] = map(list, zip(*tmparrayplus))
            tmparrayminus.sort(key=g0)
            self._locations[k][1], self._counts[k][1] = map(list, zip(*tmparrayminus))

    def merge_overlap (self):
        """merge the SAME locations. Record the duplicate number in self._counts{}

        Run it right after you add all data into this object.
        
        *Note: different with the merge_overlap() in TrackI class,
        which merges the overlapped locations.
        """
        self.total = 0
        self.total_unique = 0
        for k in self._locations.keys(): # for each chromosome
            # + strand
            plus = sorted(self._locations[k][0])
            if len(plus) <1:
                logging.warning("NO records for chromosome %s, plus strand!" % (k))
                new_plus = []
                new_plus_c = []
            else:
                (new_plus,new_plus_c) = (array(BYTE4,[plus[0]]),array(UBYTE2,[1]))
            
                pappend = new_plus.append
                pcappend = new_plus_c.append
                n = 0                # the position in new list
                for p in plus[1:]:
                    if p == new_plus[n]:
                        try:
                            new_plus_c[n]+=1
                        except OverflowError:
                            logging.warning("> 65535 + strand tags mapped to position %d on chromosome %s!" % (p,k))
                            new_plus_c[n]=65535

                    else:
                        pappend(p)
                        pcappend(1)
                        n += 1
                self.total_unique +=  len(new_plus)
                self.total += sum(new_plus_c)
            # - strand
            minus = sorted(self._locations[k][1])
            if len(minus) <1:
                logging.warning("NO records for chromosome %s, minus strand!" % (k))
                new_minus = []
                new_minus_c = []
            else:
                (new_minus,new_minus_c) = (array(BYTE4,[minus[0]]),array(UBYTE2,[1]))
            
                mappend = new_minus.append
                mcappend = new_minus_c.append
                n = 0                # the position in new list
                for p in minus[1:]:
                    if p == new_minus[n]:
                        try:
                            new_minus_c[n]+=1
                        except OverflowError:
                            logging.warning("> 65535 - strand tags mapped to position %d on chromosome %s!" % (p,k))
                            new_minus_c[n]=65535
                    else:
                        mappend(p)
                        mcappend(1)
                        n += 1
                self.total_unique +=  len(new_minus)
                self.total += sum(new_minus_c)

            self._locations[k]=[new_plus,new_minus]
            self._counts[k]=[new_plus_c,new_minus_c]
            self._well_merged = True

    def merge_plus_minus_locations_w_duplicates (self,maxnum=None):
        """Merge minus strand locations to plus strand. The duplicates
        on a single strand is defined in 'maxnum'. If maxnum is None,
        then keep all the duplicates.
                
        Side effect: Reset the counts. self.total_unique is set to
        None. This object is changed.
        """
        self.total_unique = None
        self.total = 0
        for chrom in self._locations.keys():
            (plus_tags,minus_tags) = self._locations[chrom]
            (plus_counts,minus_counts) = self._counts[chrom]

            new_plus_tags = array(BYTE4,[])
            new_plus_counts = array(UBYTE2,[])

            ip = 0
            im = 0
            lenp = len(plus_tags)
            lenm = len(minus_tags)
            while ip < lenp and im < lenm:
                if plus_tags[ip] < minus_tags[im]:
                    for i in xrange(plus_counts[ip]):
                        if maxnum and i+1>maxnum:
                            break
                        new_plus_tags.append(plus_tags[ip])
                        new_plus_counts.append(1)
                    ip += 1
                else:
                    for i in xrange(minus_counts[im]):
                        if maxnum and i+1>maxnum:
                            break
                        new_plus_tags.append(minus_tags[im])
                        new_plus_counts.append(1)                        
                    im += 1
            for im2 in xrange(im,lenm):
                # add rest of minus tags
                for i in xrange(minus_counts[im2]):
                    if maxnum and i+1>maxnum:
                        break
                    new_plus_tags.append(minus_tags[im2])
                    new_plus_counts.append(1)
                    
            for ip2 in xrange(ip,lenp):
                # add rest of minus tags
                for i in xrange(plus_counts[ip2]):
                    if maxnum and i+1>maxnum:
                        break
                    new_plus_tags.append(plus_tags[ip2])
                    new_plus_counts.append(1)
                    
            self._locations[chrom] = [new_plus_tags,[]]
            self._counts[chrom] = [new_plus_counts,[]]
            self.total += len(new_plus_tags)

    def sample (self, percent):
        """Sample the tags for a given percentage.

        Warning: the current object is changed!
        
        Side effect: self.total_unique is set to None, and counts are unset.
        """
        self.total = 0
        self.total_unique = None
        for key in self._locations.keys():
            num = int(len(self._locations[key][0])*percent)
            self._locations[key][0]=array(BYTE4,sorted(random_sample(self._locations[key][0],num)))
            num = int(len(self._locations[key][1])*percent)
            self._locations[key][1]=array(BYTE4,sorted(random_sample(self._locations[key][1],num)))
            self.total += len(self._locations[key][0]) + len(self._locations[key][1])
            self._counts[key] = [[],[]]
            
    def __str__ (self):
        return self._to_wiggle()
        
    def _to_wiggle (self):
        """Use a lot of memory!
        
        """
        t = "track type=wiggle_0 name=\"tag list\" description=\"%s\"\n" % (self.annotation)
        for k in self._locations.keys():
            (tmparrayplus,tmparrayminus) = self.get_loc_counts_by_chr(k)

            if self._locations[k][0]:
                t += "variableStep chrom=%s span=%d strand=0\n" % (k,self.fw)
                for (i,j) in tmparrayplus:
                    t += "%d\t%d\n" % (i,j)
            if self._locations[k][1]:
                t += "variableStep chrom=%s span=%d strand=1\n" % (k,self.fw)
                for (i,j) in tmparrayminus:
                    t += "%d\t%d\n" % (i,j)
        return t


class WigTrackI:
    """Designed only for wig files generated by AREM/pMA2C/MAT(future
    version). The limitation is 'span' parameter for every track must
    be the same.
    
    """
    def __init__ (self):
        self._data = {}
        self.span=0
        self.maxvalue =-10000
        self.minvalue = 10000

    def add_loc (self,chromosome,pos,value):
        if not self._data.has_key(chromosome):
            self._data[chromosome] = [array(BYTE4,[]),array(FBYTE4,[])] # for (pos,value)
        self._data[chromosome][0].append(pos)
        self._data[chromosome][1].append(value)
        if value > self.maxvalue:
            self.maxvalue = value
        if value < self.minvalue:
            self.minvalue = value
        
    def sort (self):
        """Naive sorting for tags. After sorting, counts are massed
        up.

        Note: counts are massed up, so they will be set to 1 automatically.
        """
        for k in self._data.keys():
            self._data[k] = sorted(self._data[k])
            

    def get_data_by_chr (self, chromosome):
        """Return array of counts by chromosome.

        The return value is a tuple:
        ([pos],[value])
        """
        if self._data.has_key(chromosome):
            return self._data[chromosome]
        else:
            return None
            #raise Exception("No such chromosome name (%s) in TrackI object!\n" % (chromosome))

    def get_chr_names (self):
        """Return all the chromosome names stored.
        
        """
        l = set(self._data.keys())
        return l

    def write_wig (self, fhd, name, shift=0):
        """Write all data to fhd in Wiggle Format.

        shift will be used to shift the coordinates. default: 0
        """
        chrs = self.get_chr_names()
        fhd.write("track type=wiggle_0 name=\"%s\"\n" % (name))
        for chrom in chrs:
            fhd.write("variableStep chrom=%s span=%d\n" % (chrom,self.span))
            (p,s) = self._data[chrom]
            pnext = iter(p).next
            snext = iter(s).next            
            for i in xrange(len(p)):
                pos = pnext()
                score = snext()
                fhd.write("%d\t%.4f\n" % (pos+shift,score))                

    def filter_score (self, cutoff=0):
        """Filter using a score cutoff. Return a new WigTrackI.
        
        """
        ret = WigTrackI()
        ret.span = self.span
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]

            ret._data[chrom] = [array(BYTE4,[]),array(FBYTE4,[])]
            (np,ns) = ret._data[chrom]
            npa = np.append
            nsa = ns.append

            pnext = iter(p).next
            snext = iter(s).next            
            for i in xrange(len(p)):
                pos = pnext()
                score = snext()
                if score > cutoff:
                    npa(pos)
                    nsa(score)
        return ret

    def filter_score_below (self, cutoff=0):
        """Keep points below a score cutoff. Return a new WigTrackI.
        
        """
        ret = WigTrackI()
        ret.span = self.span
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]

            ret._data[chrom] = [array(BYTE4,[]),array(FBYTE4,[])]
            (np,ns) = ret._data[chrom]
            npa = np.append
            nsa = ns.append

            pnext = iter(p).next
            snext = iter(s).next            
            for i in xrange(len(p)):
                pos = pnext()
                score = snext()
                if score < cutoff:
                    npa(pos)
                    nsa(score)
        return ret

    def write_gff (self, fhd, shift=0, source=".", feature="."):
        """Write all data to fhd in GFF format.

        shift will be used to shift the coordinates. default: 0
        """
        assert isinstance(fhd,file)
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]
            for i in xrange(len(p)):
                pi = p[i]
                si = s[i]
                fhd.write(
                    "\t".join( (chrom,source,feature,
                                str(pi-shift),str(pi-shift+self.span-1),
                                str(si),'+','.'
                                ) )+"\n"
                    )

    def write_bed (self, fhd):
        """Write all data to fhd in BED format.
        
        """
        pass

    def remove_redundant (self):
        """Remove redundant position, keep the highest score.
        
        """
        chrs = set(self._data.keys())
        ndata = {}
        for chrom in chrs:
            ndata[chrom] = [array(BYTE4,[]),array(FBYTE4,[])] # for (pos,value)
            nd_p_append = ndata[chrom][0].append
            nd_s_append = ndata[chrom][1].append
            (p,s) = self._data[chrom]
            prev_p = None
            prev_s = None
            for i in xrange(len(p)):
                pi = p[i]
                si = s[i]
                if not prev_p:
                    prev_p = pi
                    prev_s = si
                else:
                    if pi == prev_p:
                        if si>prev_s:
                            prev_s = si
                    else:
                       nd_p_append (prev_p)
                       nd_s_append (prev_s)
            nd_p_append (prev_p)
            nd_s_append (prev_s)
        del self._data
        self._data = ndata

    def find_peaks (self, bw=None):
        """A naive peak finding algorithm to find all local maximum
        points.

        bw : Bandwidth. Two local maximums will compete if their
        distance is less than bw. The higher one will be kept, or if
        they are equal, the last point will be kept. Default is 4*span.

        Return type:
        
        find_peak will return a new WigTrackI object with position
        and score for each local maximum(peaks).
        """
        if not bw:
            bw = 4*self.span
        bw = max(1,bw)
        ret = WigTrackI()
        ret.span = 1
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]
            prev_peak_p = -10000
            prev_peak_s = -10000
            prev_peak_summits = []
            prev_p = -10000
            prev_s = -10000
            increase = False
            for i in xrange(len(p)):
                pi = p[i]
                si = s[i]
                if si > prev_s:
                    # increase
                    increase = True
                elif si < prev_s:
                    # decrease
                    if increase:
                        # prev_p is a summit
                        #print prev_p,prev_s,pi,si
                        if prev_p-prev_peak_p < bw:
                            # two summits are near
                            if prev_s > prev_peak_s:
                                # new summit is high
                                prev_peak_s = prev_s
                                prev_peak_p = prev_p
                        else:
                            # it's a new summit
                            #print chrom,prev_peak_p,prev_peak_s
                            try:
                                ret.add_loc(chrom,prev_peak_p,prev_peak_s)
                            except OverflowError:
                                pass
                            prev_peak_s = prev_s
                            prev_peak_p = prev_p
                            
                    increase = False
                prev_p = pi
                prev_s = si
            try:
                ret.add_loc(chrom,prev_peak_p,prev_peak_s)            
            except OverflowError:
                pass
        return ret

    def find_valleys (self, bw=None):
        """A naive peak finding algorithm to find all local minimum
        points.

        bw : Bandwidth. Two local maximums will compete if their
        distance is less than bw. The higher one will be kept, or if
        they are equal, the last point will be kept. Default is 4*span.

        Return type:
        
        find_peak will return a new WigTrackI object with position
        and score for each local maximum(peaks).
        """
        if not bw:
            bw = 4*self.span
        bw = max(1,bw)
        ret = WigTrackI()
        ret.span = 1
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]
            prev_peak_p = -10000
            prev_peak_s = -10000
            prev_peak_summits = []
            prev_p = -10000
            prev_s = -10000
            decrease = False
            for i in xrange(len(p)):
                pi = p[i]
                si = s[i]
                if si < prev_s:
                    # decrease
                    decrease = True
                elif si > prev_s:
                    # increase
                    if decrease:
                        # prev_p is a valley
                        #print prev_p,prev_s,pi,si
                        if prev_p-prev_peak_p < bw:
                            # two summits are near
                            if prev_s < prev_peak_s:
                                # new summit is lower
                                prev_peak_s = prev_s
                                prev_peak_p = prev_p
                        else:
                            # it's a new valley
                            #print chrom,prev_peak_p,prev_peak_s
                            try:
                                ret.add_loc(chrom,prev_peak_p,prev_peak_s)
                            except OverflowError:
                                pass
                            prev_peak_s = prev_s
                            prev_peak_p = prev_p
                            
                    decrease = False
                prev_p = pi
                prev_s = si
            try:
                ret.add_loc(chrom,prev_peak_p,prev_peak_s)            
            except OverflowError:
                pass
        return ret

    def total (self):
        t = 0
        chrs = set(self._data.keys())
        for chrom in chrs:
            (p,s) = self._data[chrom]
            t += len(p)
        return t

class BinKeeperI:
    """BinKeeper keeps point data from a chromosome in a bin list.

    Example:
    >>> w = WiggleIO('sample.wig')
    >>> bk = w.build_binKeeper()
    >>> bk['chrI'].pp2v(1000,2000) # to extract values in chrI:1000..2000
    """
    def __init__ (self,bin=8,chromosomesize=1e9):
        """Initializer.

        Parameters:
        bin : size of bin in Kilo Basepair
        chromosomesize : size of chromosome, default is 1G
        """
        self.binsize = bin*1024
        self.binnumber = int(chromosomesize/self.binsize)+1
        self.cage = []
        a = self.cage.append
        for i in xrange(self.binnumber):
            a([array(BYTE4,[]),array(FBYTE4,[])])

    def add ( self, p, value ):
        """Add a position into BinKeeper.

        Note: position must be sorted before adding. Otherwise, pp2v
        and pp2p will not work.
        """
        bin = p/self.binsize
        self.cage[bin][0].append(p)
        self.cage[bin][1].append(value)        

    def p2bin (self, p ):
        """Return the bin index for a position.
        
        """
        return p/self.binsize

    def p2cage (self, p):
        """Return the bin containing the position.
        
        """
        return self.cage[p/self.binsize]

    def _pp2cages (self, p1, p2):
        assert p1<=p2
        bin1 = self.p2bin(p1)
        bin2 = self.p2bin(p2)+1
        t = [array(BYTE4,[]),array(FBYTE4,[])]
        for i in xrange(bin1,bin2):
            t[0].extend(self.cage[i][0])
            t[1].extend(self.cage[i][1])            
        return t

    def pp2p (self, p1, p2):
        """Give the position list between two given positions.

        Parameters:
        p1 : start position
        p2 : end position
        Return Value:
        list of positions between p1 and p2.
        """
        (ps,vs) = self._pp2cages(p1,p2)
        p1_in_cages = bisect_left(ps,p1)
        p2_in_cages = bisect_right(ps,p2)
        return ps[p1_in_cages:p2_in_cages]

    def pp2v (self, p1, p2):
        """Give the value list between two given positions.

        Parameters:
        p1 : start position
        p2 : end position
        Return Value:
        list of values whose positions are between p1 and p2.
        """
        (ps,vs) = self._pp2cages(p1,p2)
        p1_in_cages = bisect_left(ps,p1)
        p2_in_cages = bisect_right(ps,p2)
        return vs[p1_in_cages:p2_in_cages]


    def pp2pv (self, p1, p2):
        """Give the (position,value) list between two given positions.

        Parameters:
        p1 : start position
        p2 : end position
        Return Value:
        list of (position,value) between p1 and p2.
        """
        (ps,vs) = self._pp2cages(p1,p2)
        p1_in_cages = bisect_left(ps,p1)
        p2_in_cages = bisect_right(ps,p2)
        return zip(ps[p1_in_cages:p2_in_cages],vs[p1_in_cages:p2_in_cages])
