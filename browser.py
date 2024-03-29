import dash
import dash_html_components as html
from jbrowse_jupyter import create, create_component

app = dash.Dash(__name__)

# ============ create config and pass additional params =======
jbrowse_conf = create("config")
aliases = ["hg38"]
ref_name_aliases = {
    "adapter": {
        "type": "RefNameAliasAdapter",
        "location": {
            "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/"
            "GRCh38/hg38_aliases.txt",
        },
    },
}

# ============= setting the assembly ==============
assembly_data = "https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz"
jbrowse_conf.set_assembly(assembly_data, aliases, ref_name_aliases)

# ============== adding a track ===============
track_data = "https://s3.amazonaws.com/jbrowse.org/genomes/" \
              "GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full" \
              "_analysis_set.refseq_annotation.sorted.gff.gz"
jbrowse_conf.add_track(track_data, name="test-demo")

# ============== set location ===============

jbrowse_conf.set_location("10:1..19999")

# ============== adding custom theme ===============

jbrowse_conf.set_theme("#311b92", "#0097a7", "#f57c00", "#d50000")

# ======== grab config  ========
config = jbrowse_conf.get_config()

# ========= create a dash component ==============

component = create_component(config)

# ========== launch the component ===========
app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=8080, debug=True)
