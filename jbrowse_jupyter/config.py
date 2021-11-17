from jupyter_dash import JupyterDash
import dash_jbrowse
import dash_html_components as html
import re

class JBrowseConfig():

    def __init__(self):
        self.config = {
            "assembly": {},
            "tracks": [],
            "defaultSession": {}, 
            "location": ""
        }
        self.tracks_ids_map = {}
    
    def get_config(self):
        return self.config

    def launch_jbrowse(self):
        app = JupyterDash(__name__)

        app.layout = html.Div(
            [
                dash_jbrowse.DashJbrowse(
                    id="input",
                    assembly=self.config["assembly"],
                    tracks=self.config["tracks"],
                    defaultSession=self.config["defaultSession"],
                    location=self.config["location"],
                ),
            ]
        )
        
        app.run_server(mode="inline")
    
    ########## PASS IN FILE ###########
    def set_assembly (self, assembly_data, aliases, refname_aliases, bgzip= False):
        if not bgzip:
            self.unzipped_assembly(assembly_data, aliases, refname_aliases)
        else:
            self.zipped_assembly(assembly_data, aliases, refname_aliases)
    

    def unzipped_assembly(self, assembly_data, aliases = [], refname_aliases = []):
        name = self.get_name(assembly_data)

        self.config['assembly'] = {
            "name": name,
            "sequence":{
                "type": "ReferenceSequenceTrack",
                "trackId": name + "-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {
                        "uri": assembly_data,
                    },
                    "faiLocation": {
                        "uri": assembly_data + ".fai",
                    },
                },
            },
            "aliases":aliases,
            "refNameAliases": refname_aliases
        }
    
    def zipped_assembly(self, assembly_data, aliases, refname_aliases):
        name = self.get_name(assembly_data)
        print('name:' + name)
        self.config['assembly'] = {
            "name": name,
            "sequence":{
                "type": "ReferenceSequenceTrack",
                "trackId": name + "-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {
                        "uri": assembly_data,
                    },
                    "faiLocation": {
                        "uri": assembly_data + ".fai",
                    },
                    "gziLocation": {
                        "uri": assembly_data + ".gzi",
                    },
                },
            },
            "aliases":aliases,
            "refNameAliases": refname_aliases
        }
    

    def get_name(self, assembly_file):
        return re.search(r'(\w+)\.(?:fa|fasta|fa\.gz)$', assembly_file).group(1)
    
    ########## CORRECT DEFAULT SESSION ###########
    def set_default_session(self, assembly, displayed_tracks, display_assembly=True):
        reference_track = self.get_reference_track(assembly, display_assembly)
        #tracks = self.get_tracks(assembly, displayed_tracks, display_assembly)
        self.config["defaultSession"] = {
            "name": "my session",
            "view": {
                "id": "LinearGenomeView",
                "type": "LinearGenomeView",
                "tracks": reference_track
            }
        }

    def get_reference_track(self, assembly, display_assembly):
        assembly_name = assembly["name"]
        configuration = assembly_name + "-ReferenceSequenceTrack"
        ref = {}
        if display_assembly:
            ref = {
                "type": "ReferenceSequenceTrack",
                "configuration": configuration,
                "displays": [
                    {
                        "type": "LinearBasicDisplay",
                        "configuration": configuration + "-LinearBasicDisplay"
                    }
                ],

            }
        return ref

    ########## CORRECT LOCATION ########
    def set_location(self, location=""):
        self.config["location"] = location
            
