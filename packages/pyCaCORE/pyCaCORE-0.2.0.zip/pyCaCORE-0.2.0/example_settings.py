
# The location of the input WSDL
WSDL_FILE = "conf/cabio.wsdl"

# Root package for the resulting API 
ROOT_PACKAGE = "cabio"

# Mapping from Java to Python packages 
# The ROOT_PACKAGE is prepended to each Python package
PACKAGE_MAPPING = {
    'gov.nih.nci.cabio.domain' : 'domain',
    'gov.nih.nci.common.domain' : 'common.domain',
    'gov.nih.nci.common.provenance.domain' : 'common.provenance.domain',
}

# Main API entry point
SERVICE_CLASS_NAME = "CaBioApplicationService"

# Output directory for generated API
OUTPUT_DIR = "output"
