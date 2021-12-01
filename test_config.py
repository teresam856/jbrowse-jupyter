import unittest
from jbrowse_jupyter.jbrowse_config import JBrowseConfig

class TestConfig(unittest.TestCase):

    def __init__(self, config_obj):
        self.config_obj = config_obj

    def test_human(self):
        ref_name = {
            "adapter": {
                "type": "RefNameAliasAdapter",
                "location": {
                    "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
                }
            }
        }
        aliases = [
            "GRCh37"
        ]
        self.config_obj.set_assembly("https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz", aliases, ref_name, True)
        assembly = self.config_obj.get_assembly()
        self.assertEqual(assembly["name"], "hg19")
        self.assertEqual(assembly["aliases"], [
            "GRCh37"
        ])
        self.assertEqual(assembly["sequence"], {
            "type": "ReferenceSequenceTrack",
            "trackId": "Pd8Wh30ei9R",
            "adapter": {
                "type": "BgzipFastaAdapter",
                "fastaLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
                },
                "faiLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.fai"
                },
                "gziLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.gzi"
                }
            }
        })
        self.assertEqual(assembly["sequence"]["type"], "ReferenceSequenceTrack")
        self.assertEqual(assembly["sequence"]["trackId"], "Pd8Wh30ei9R")
        self.assertEqual(assembly["sequence"]["adapter"], {
                "type": "BgzipFastaAdapter",
                "fastaLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
                },
                "faiLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.fai"
                },
                "gziLocation": {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.gzi"
                }
            })
        self.assertEqual(assembly["sequence"]["adapter"]["type"], "BgzipFastaAdapter")
        self.assertEqual(assembly["sequence"]["adapter"]["fastaLocation"], {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
                })
        self.assertEqual(assembly["sequence"]["adapter"]["faiLocation"], {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.fai"
                })
        self.assertEqual(assembly["sequence"]["adapter"]["gziLocation"], {
                    "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.gzi"
                })
        self.assertEqual(assembly["refNameAliases"], {
            "adapter": {
                "type": "RefNameAliasAdapter",
                "location": {
                    "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
                }
            }
        })
        self.assertEqual(assembly["refNameAliases"]["adapter"], {
                "type": "RefNameAliasAdapter",
                "location": {
                    "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
                }})
        self.assertEqual(assembly["refNameAliases"]["adapter"]["type"], "RefNameAliasAdapter")
        self.assertEqual(assembly["refNameAliases"]["adapter"]["location"], {
                    "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
                })
        
        self.config_obj.set_default_session(assembly, None)
        session = self.config_obj.get_config()["defaultSession"]
        self.assertEqual(session["name"], "my session")
        self.assertEqual(session["view"], {
                "id": "LinearGenomeView",
                "type": "LinearGenomeView",
                "tracks": {
                    "type": "ReferenceSequenceTrack",
                    "configuration": "hg19-ReferenceSequenceTrack",
                    "displays": [
                        {
                            "type": "LinearBasicDisplay",
                            "configuration": "hg19-ReferenceSequenceTrack" + "-LinearBasicDisplay"
                        }
                    ],

                }
            })
        
    # def test_location(self):

if __name__ == "__main__":
    config_obj = JBrowseConfig()
    test = TestConfig(config_obj)
    test.test_config()
    # test.test_session()
    # test.test_assembly()
    # test.test_location()
        
