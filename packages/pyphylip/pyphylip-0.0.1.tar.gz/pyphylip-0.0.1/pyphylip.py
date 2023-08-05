"""Read and write files in the phylip sequence format.

The taxa names in a phylip file can be at most ten characters long.
If they are exactly ten characters then they butt up against the sequence.
http://www.life.umd.edu/labs/delwiche/MSyst/lec/phylip.html
http://www.molecularevolution.org/resources/fileformats/phylip_dna
"""

import unittest
from StringIO import StringIO
import textwrap

pyphylip_version = '0.0.1'

g_phylip_string = """
7 50
thermotogaATGGCGAAGGAAAAATTTGTGAGAACAAAACCGCATGTTAACGTTGGAAC
TthermophiATGGCGAAGGGCGAGTTTGTTCGGACGAAGCCTCACGTGAACGTGGGGAC
TaquaticusATGGCGAAGGGCGAGTTTATCCGGACGAAGCCCCACGTGAACGTGGGGAC
deinonema-ATGGCTAAGGGAACGTTTGAACGCACCAAACCCCACGTGAACGTGGGCAC
ChlamydiaBATGTCAAAAGAAACTTTTCAACGTAATAAGCCTCATATCAACATAGGGGC
flexistipsATGTCCAAGCAAAAGTACGAAAGGAAGAAACCTCACGTAAACGTAGGCAC
borrelia-bATGGCAAAAGAAGTTTTTCAAAGAACAAAGCCGCACATGAATGTTGGAAC
""".strip()

g_headers = [
        'thermotoga',
        'Tthermophi',
        'Taquaticus',
        'deinonema-',
        'ChlamydiaB',
        'flexistips',
        'borrelia-b']

g_sequences = [
        'ATGGCGAAGGAAAAATTTGTGAGAACAAAACCGCATGTTAACGTTGGAAC',
        'ATGGCGAAGGGCGAGTTTGTTCGGACGAAGCCTCACGTGAACGTGGGGAC',
        'ATGGCGAAGGGCGAGTTTATCCGGACGAAGCCCCACGTGAACGTGGGGAC',
        'ATGGCTAAGGGAACGTTTGAACGCACCAAACCCCACGTGAACGTGGGCAC',
        'ATGTCAAAAGAAACTTTTCAACGTAATAAGCCTCATATCAACATAGGGGC',
        'ATGTCCAAGCAAAAGTACGAAAGGAAGAAACCTCACGTAAACGTAGGCAC',
        'ATGGCAAAAGAAGTTTTTCAAAGAACAAAGCCGCACATGAATGTTGGAAC']

class PhylipError(Exception):
    pass

def get_lines(raw_lines):
    """
    @param raw_lines: raw lines
    @return: a list of nonempty lines
    """
    lines = [x.rstrip('\r\n') for x in raw_lines]
    return [x for x in lines if x]

def nunique_lengths(seq_of_seq):
    """
    Given a sequence of sequences, return the number of unique lengths.
    @param: a sequence of sequences
    @return: the number of unique sequence lengths
    """
    return len(set(len(seq) for seq in seq_of_seq))

def decode(raw_lines):
    """
    This parses lines of a non-interleaved phylip sequence file.
    @param raw_lines: raw lines of a non-interleaved phylip alignment file
    @return: headers, sequences
    """
    lines = get_lines(raw_lines)
    header_line, data_lines = lines[0], lines[1:]
    header_row = header_line.split()
    if len(header_row) != 2:
        raise PhylipError('the header should be a line with two integers')
    ntaxa_s, ncolumns_s = header_row
    try:
        ntaxa = int(ntaxa_s)
        ncolumns = int(ncolumns_s)
    except ValueError:
        raise PhylipError('the header should be a line with two integers')
    # check the number of data lines
    ntaxa_observed = len(data_lines)
    if ntaxa_observed != ntaxa:
        msg_a = 'the header says there are %d taxa' % ntaxa
        msg_b = 'but %d taxa were observed' % ntaxa_observed
        raise PhylipError(msg_a + msg_b)
    # all line lengths should be the same
    if nunique_lengths(data_lines) != 1:
        raise PhylipError('all data lines should be the same length')
    # break lines into taxa and data
    compound_data_rows = [[x[:10].strip(), x[10:].strip()] for x in data_lines]
    headers, sequences = zip(*compound_data_rows)
    ncolumns_observed = len(sequences[0])
    if ncolumns_observed != ncolumns:
        msg_a = 'the header says there are %d alignment columns' % ncolumns
        msg_b = 'but %d alignment columns were observed' % ncolumns_observed
        raise PhylipError(msg_a + msg_b)
    return headers, sequences

def encode(headers, sequences):
    """
    This creates the contents of a non-interleaved phylip sequence file.
    @param headers: some header strings
    @param sequences: some sequence strings
    """
    nrows = len(headers)
    ncols = len(sequences[0])
    out_lines = ['%d %d' % (nrows, ncols)]
    for h, seq in zip(headers, sequences):
        out_h = h[:10].ljust(10)
        out_lines.append(out_h + seq)
    return '\n'.join(out_lines)


class TestPhylip(unittest.TestCase):

    def test_decode(self):
        headers, sequences = decode(g_phylip_string.splitlines())
        self.assertEqual(list(headers), g_headers)
        self.assertEqual(list(sequences), g_sequences)

    def test_encode(self):
        blob = encode(g_headers, g_sequences)
        self.assertEqual(blob, g_phylip_string)

    def test_write_long_headers(self):
        long_headers = [
                'thermotogawat',
                'Tthermophiwat',
                'Taquaticusfoo',
                'deinonema-x',
                'ChlamydiaBxxxxxx',
                'flexistipsyy',
                'borrelia-by']
        blob = encode(long_headers, g_sequences)
        self.assertEqual(blob, g_phylip_string)

    def test_write_short_headers(self):
        short_headers = [
                'thermot',
                'Tthermo',
                'Taquati',
                'deinone',
                'Chlamyd',
                'flexist',
                'borreli']
        expected_blob = textwrap.dedent("""
        7 50
        thermot   ATGGCGAAGGAAAAATTTGTGAGAACAAAACCGCATGTTAACGTTGGAAC
        Tthermo   ATGGCGAAGGGCGAGTTTGTTCGGACGAAGCCTCACGTGAACGTGGGGAC
        Taquati   ATGGCGAAGGGCGAGTTTATCCGGACGAAGCCCCACGTGAACGTGGGGAC
        deinone   ATGGCTAAGGGAACGTTTGAACGCACCAAACCCCACGTGAACGTGGGCAC
        Chlamyd   ATGTCAAAAGAAACTTTTCAACGTAATAAGCCTCATATCAACATAGGGGC
        flexist   ATGTCCAAGCAAAAGTACGAAAGGAAGAAACCTCACGTAAACGTAGGCAC
        borreli   ATGGCAAAAGAAGTTTTTCAAAGAACAAAGCCGCACATGAATGTTGGAAC
        """).strip()
        blob = encode(short_headers, g_sequences)
        self.assertEqual(blob, expected_blob)


if __name__ == '__main__':
    unittest.main()
