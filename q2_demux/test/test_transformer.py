import unittest
import tempfile

from q2_demux._format import (EMPMultiplexedDirFmt,
                              EMPMultiplexedSingleEndDirFmt)
from q2_demux._demux import BarcodeSequenceIterator
from q2_types.testing import TestPluginBase


class TestTransformers(TestPluginBase):
    package = 'q2_demux.test'

    def setUp(self):
        # TODO generalize plugin lookup when ported to framework. This code
        # is adapted from the base class.
        try:
            from q2_demux.plugin_setup import plugin
        except ImportError:
            self.fail("Could not import plugin object.")

        self.plugin = plugin

        # TODO use qiime temp dir when ported to framework, and when the
        # configurable temp dir exists
        self.temp_dir = tempfile.TemporaryDirectory(
            prefix='q2-demux-test-temp-')

    def test_emp_multiplexed_format_barcode_sequence_iterator(self):
        transformer = self.get_transformer(EMPMultiplexedDirFmt,
                                           BarcodeSequenceIterator)
        dirname = 'emp_multiplexed'
        dirpath = self.get_data_path(dirname)
        bsi = transformer(EMPMultiplexedDirFmt(dirpath, mode='r'))
        bsi = list(bsi)
        self.assertEqual(len(bsi), 250)
        # this code is commented, pending merge of qiime2/q2-demux#4, when
        # the data type will change to match what I have here.
        # self.assertEqual(
        #     bsi[0][0],
        #     ['@M00176:17:000000000-A0CNA:1:1:15487:1773 1:N:0:0\n',
        #      'TTAGGCATCTCG\n',
        #      '+\n',
        #      'B@@FFFFFHHHH\n'])
        # self.assertEqual(
        #     bsi[0][1],
        #     ['@M00176:17:000000000-A0CNA:1:1:15487:1773 1:N:0:0\n',
        #      'GCTTAGGGATTTTATTGTTATCAGGGTTAATCGTGCCAAGAAAAGCGGCATGGTCAATATAAC'
        #      'CAGTAGTGTTAACAGTCGGGAGAGGAGTGGCATTAACACCATCCTTCATGAACTTAATCCACT'
        #      'GTTCACCATAAACGTGACGATGAGG',
        #      '+',
        #      'C@CFFFFFHHFHHGIJJ?FFHEIIIIHGEIIFHGIIJHGIGBGB?DHIIJJJJCFCHIEGIGG'
        #      'HGFAEDCEDBCCEEA.;>?BB=288A?AB709@:3:A:C88CCD@CC444@>>34>>ACC:?C'
        #      'CD<CDCA>A@A>:<?B@?<((2(>?'])

    def test_emp_se_multiplexed_format_barcode_sequence_iterator(self):
        transformer1 = self.get_transformer(EMPMultiplexedSingleEndDirFmt,
                                            EMPMultiplexedDirFmt)
        transformer2 = self.get_transformer(EMPMultiplexedDirFmt,
                                            BarcodeSequenceIterator)
        dirname = 'emp_multiplexed_single_end'
        dirpath = self.get_data_path(dirname)
        emp_demultiplexed = \
            transformer1(EMPMultiplexedSingleEndDirFmt(dirpath, mode='r'))
        bsi = transformer2(EMPMultiplexedDirFmt(emp_demultiplexed, mode='r'))
        bsi = list(bsi)
        self.assertEqual(len(bsi), 250)
        # this code is commented, pending merge of qiime2/q2-demux#4, when
        # the data type will change to match what I have here.
        # self.assertEqual(
        #     bsi[0][0],
        #     ['@M00176:17:000000000-A0CNA:1:1:15487:1773 1:N:0:0\n',
        #      'TTAGGCATCTCG\n',
        #      '+\n',
        #      'B@@FFFFFHHHH\n'])
        # self.assertEqual(
        #     bsi[0][1],
        #     ['@M00176:17:000000000-A0CNA:1:1:15487:1773 1:N:0:0\n',
        #      'GCTTAGGGATTTTATTGTTATCAGGGTTAATCGTGCCAAGAAAAGCGGCATGGTCAATATAAC'
        #      'CAGTAGTGTTAACAGTCGGGAGAGGAGTGGCATTAACACCATCCTTCATGAACTTAATCCACT'
        #      'GTTCACCATAAACGTGACGATGAGG',
        #      '+',
        #      'C@CFFFFFHHFHHGIJJ?FFHEIIIIHGEIIFHGIIJHGIGBGB?DHIIJJJJCFCHIEGIGG'
        #      'HGFAEDCEDBCCEEA.;>?BB=288A?AB709@:3:A:C88CCD@CC444@>>34>>ACC:?C'
        #      'CD<CDCA>A@A>:<?B@?<((2(>?'])

    def test_invalid(self):
        dirname = 'bad'
        dirpath = self.get_data_path(dirname)
        transformer = self.get_transformer(EMPMultiplexedDirFmt,
                                           BarcodeSequenceIterator)
        with self.assertRaises(ValueError):
            transformer(EMPMultiplexedDirFmt(dirpath, mode='r'))

        transformer = self.get_transformer(EMPMultiplexedSingleEndDirFmt,
                                           EMPMultiplexedDirFmt)
        with self.assertRaises(ValueError):
            transformer(EMPMultiplexedSingleEndDirFmt(dirpath, 'r'))

if __name__ == "__main__":
    unittest.main()