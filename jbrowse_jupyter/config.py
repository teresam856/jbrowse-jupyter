from jupyter_dash import JupyterDash
import dash_jbrowse
import dash_html_components as html
import re
from django.core.validators import URLValidator, ValidationError
from jbrowse_jupyter.server import launch

class JBrowseConfig():

    def __init__(self):
        self.config = {
            "assembly": {},
            "tracks": [],
            "defaultSession": {}, 
            "location": ""
        }
        self.tracks_ids_map = {}
    
    # TODO: do we want to check this here or in dash_jbrowse?
    def valid_url(self, file):
        validate = URLValidator()
        try:
            validate(file)
            return True
        except ValidationError as exception:
            return False
    
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
        if self.valid_url(assembly_data):
            if not bgzip:
                self.unzipped_assembly(assembly_data, aliases, refname_aliases)
            else:
                self.zipped_assembly(assembly_data, aliases, refname_aliases)
        else:
            # launch flask server
            launch()
            # figure out passing url, etc

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

    
            
